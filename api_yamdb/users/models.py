import string
import random

from django.db import models
from django.contrib.auth.models import AbstractUser


ROLES = (
        ('admin', 'Админ'),
        ('user', 'Пользователь'),
        ('moderator', 'Модератор'),
)

CODE_LENGTH = 12


def generate_conf_code(length):
    """Генератор кода подтверждения."""
    conf_code = ''.join(
        [random.choice(
            string.ascii_uppercase + string.digits
        )for num in range(length)]
    )
    return conf_code


class User(AbstractUser):
    """Модель пользователя."""
    username = models.CharField(
        'Имя пользователя',
        max_length=150, unique=True,
        help_text='Придумайте логин.'
    )
    email = models.EmailField(
        'Адрес электронной почты',
        max_length=254,
        blank=False,
        null=False,
        help_text='Введите email'
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
        blank=True,
        null=True,
        help_text='Введите имя'
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        blank=True,
        null=True,
        help_text='Введите фамилию.'
    )
    bio = models.TextField(
        'О себе',
        blank=True
    )
    role = models.CharField(
        'Роль пользователя',
        max_length=25,
        choices=ROLES,
        default='user',
        help_text='Выберите роль.'
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=50,
        null=True,
        default=generate_conf_code(CODE_LENGTH),
        help_text='Ваш код подтверждения.'
    )

    @property
    def is_user(self):
        """Роль пользователя."""
        return self.role == 'user'

    @property
    def is_moderator(self):
        """Роль модератора."""
        return self.role == 'moderator'

    @property
    def is_admin(self):
        """Роль админа."""
        return self.role == 'admin'
