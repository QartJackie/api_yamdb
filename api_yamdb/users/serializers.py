from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.core.exceptions import ValidationError

from .models import User


class GetTokenSerializer(serializers.Serializer):
    """Сериализатор токена."""

    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)


class UserSerializer(serializers.Serializer):
    """Сериализатор User'ов."""

    email = serializers.EmailField(required=True, max_length=254)
    username = serializers.SlugField(required=True, max_length=150)

    def validate(self, validated_data):
        """Валидация логина."""

        if validated_data['username'] == 'me':
            raise ValidationError('Данное имя недоступно')
        return validated_data

    def create(self, validated_data):
        """Функция добавления пользователя."""

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email']
        )
        return user

    class Meta:
        """Настройка выдачи."""

        model = User
        fields = ('email', 'username')


class UserSearchSerializer(serializers.ModelSerializer):
    """Сериализатор выдачи пользоватлей."""

    email = serializers.EmailField(
        required=True,
        max_length=254,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.SlugField(
        required=True, max_length=150,
        validators=[
            UniqueValidator(queryset=User.objects.all()),
        ]
    )

    def validate(self, validated_data):
        """Проверка поля username."""

        username = validated_data.get('username', None)
        if username == 'me':
            raise ValidationError('Данное имя недоступно')
        return validated_data

    def create(self, validated_data):
        """Создание модели поьзователя."""

        user = User.objects.create_user(
            **validated_data
        )
        return user

    class Meta:
        """Настройка выдачи."""

        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'role', 'bio'
        )


class MeSerializer(serializers.ModelSerializer):
    """Сериализатор модели User."""

    email = serializers.EmailField(
        required=True,
        max_length=254,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.SlugField(
        required=True, max_length=150,
        validators=[
            UniqueValidator(queryset=User.objects.all()),
        ]
    )

    def validate(self, validated_data):
        """Валидатор логина."""

        username = validated_data.get('username', None)
        if username == 'me':
            raise ValidationError('Данное имя недоступно')
        return validated_data

    def create(self, validated_data):
        """Создание пользователя."""

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email']
        )
        return user

    class Meta:
        """Настройка выдачи."""

        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'role', 'bio'
        )
        read_only_fields = ('role',)
