from django.db import models
from django.contrib.auth.models import AbstractUser


ROLES = (
        ('admin', 'Админ'),
        ('user', 'Пользователь'),
        ('moderator', 'Модератор'),
)


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(
        'Адрес электронной почты',
        max_length=254,
        unique=True,
        blank=False,
        null=False
    )
    first_name = models.CharField('Имя', max_length=150)
    last_name = models.CharField('Фамилия', max_length=150)
    bio = models.TextField(
        'О себе',
        blank=True
    )
    role = models.CharField(
        'Роль пользователя',
        max_length=25,
        choices=ROLES,
        default='user'
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
