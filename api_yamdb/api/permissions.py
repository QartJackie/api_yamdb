from rest_framework import permissions

from users.models import User

class AuthorAdminModerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.is_authenticated and request.method != 'PUT'
            )
        )

    def has_object_permission(self, request, view, obj):
        if (request.method in permissions.SAFE_METHODS or
            obj.author == request.user):
                return True
        user=User.objects.get(username=request.user)
        return user.role in ('admin','moderator')
