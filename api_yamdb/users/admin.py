from django.contrib import admin
from users.models import User


class UserAdmin(admin.ModelAdmin):
    """Регистрация модели пользователя."""
    list_display = (
        'id',
        'first_name',
        'last_name',
        'username',
        'email',
        'bio',
        'role'
    )
    list_filter = ('role',)
    search_fields = ('username', 'first_name', 'last_name', 'email')


admin.site.register(User, UserAdmin)
