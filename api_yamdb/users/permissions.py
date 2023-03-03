from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    message = 'Недостаточно прав'

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_admin or request.user.is_superuser
        )


class IsModerator(permissions.BasePermission):
    message = 'Недостаточно прав'

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_moderator or request.user.is_superuser
        )


class IsAuthorOrReadOnly(permissions.BasePermission):
    message = 'Недостаточно прав'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class IsAuthorOrAdminOrReadOnly(permissions.BasePermission):
    message = 'Недостаточно прав'

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            and request.user.is_anonymous
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_admin
            or request.user.is_moderator
        )
