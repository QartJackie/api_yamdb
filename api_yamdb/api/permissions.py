from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Все не безопасные методы доступны только админу."""

    message = 'Недостаточно прав'

    def has_permission(self, request, view):
        """обощеуровневое разрешение."""
        return ((request.user.is_authenticated
                 and (request.user.is_admin or request.user.is_superuser)
                 ) or request.method in permissions.SAFE_METHODS)


class AuthorAdminModerOrReadOnly(permissions.BasePermission):
    """Не безопасные методы доступны только админу, модератору и автору."""

    message = 'Недостаточно прав'

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated)
                )

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or request.user.is_admin
                or request.user.is_moderator)
