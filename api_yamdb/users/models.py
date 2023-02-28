from django.db import models
from django.contrib.auth.models import AbstractUser


ROLES = (
        ('admin', 'Админ'),
        ('user', 'Пользователь'),
        ('moderator', 'Модератор'),
)


class User(AbstractUser):
    role = models.CharField(
        'Роль пользователя',
        max_length=25,
        choices=ROLES,
        default='user'
    )
    bio = models.TextField(
        'О себе',
        blank=True
    ),
    email = models.EmailField(
        'Адрес электронной почты',
        max_length=254,
        unique=True,
        blank=False,
        null=False
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=50,
        null=True
    )

    @property
    def is_user(self):
        return self.role == 'user'

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    @property
    def is_admin(self):
        return self.role == 'admin'
