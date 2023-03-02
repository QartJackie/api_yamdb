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
    conf_code = ''.join(
        [random.choice(
            string.ascii_uppercase + string.digits
        )for num in range(length)]
    )
    return conf_code


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(
        'Адрес электронной почты',
        max_length=254,
        unique=True,
        blank=False,
        null=False
    )
    first_name = models.CharField(
        'Имя', max_length=150, blank=True, null=True
    )
    last_name = models.CharField(
        'Фамилия', max_length=150, blank=True, null=True
    )
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
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=50,
        null=True,
        default=generate_conf_code(CODE_LENGTH)
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
