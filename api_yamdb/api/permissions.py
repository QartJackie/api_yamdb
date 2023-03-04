from rest_framework import permissions
from users.models import User


class IsAdminOrReadOnly(permissions.BasePermission):
    """Все не безопасные методы доступны только админу."""

    message = 'Недостаточно прав'

    def has_permission(self, request, view):
        """обощеуровневое разрешение."""
        return (
                (request.user.is_authenticated
                 and (request.user.is_admin or request.user.is_superuser)
                 ) or request.method in permissions.SAFE_METHODS
            )


class AuthorAdminModerOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated and request.method != 'PUT')
                )

    def has_object_permission(self, request, view, obj):
        if (request.method in permissions.SAFE_METHODS
           or obj.author == request.user):
            return True
        user = User.objects.get(username=request.user)
        return user.role in ('admin', 'moderator')
