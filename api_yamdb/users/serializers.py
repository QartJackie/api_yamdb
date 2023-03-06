from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.core.exceptions import ValidationError

from .models import User


class BaseUserSerializer(serializers.ModelSerializer):
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


class GetTokenSerializer(serializers.Serializer):
    """Сериализатор токена."""

    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)


class UserSerializer(BaseUserSerializer):
    """Сериализатор User'ов."""

    email = serializers.EmailField(required=True, max_length=254)
    username = serializers.SlugField(required=True, max_length=150)

    def validate(self, data):
        """Валидация уникальности полей"""
        users_username = User.objects.filter(username=data['username'])
        users_email = User.objects.filter(email=data['email'])
        if data['username'] == 'me':
            raise ValidationError('Данное имя недоступно')
        elif users_username.exclude(
            email=data['email'], username=data['username']
        ).exists():
            raise serializers.ValidationError(
                "Юзернейм должен быть уникальным"
            )
        elif users_email.exclude(
            username=data['username'], email=data['email']
        ).exists():
            raise serializers.ValidationError("Эмейл должен быть уникальным")
        return data

    class Meta:
        """Настройка выдачи."""

        model = User
        fields = ('email', 'username')


class UserSearchSerializer(BaseUserSerializer):
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

    class Meta:
        """Настройка выдачи."""

        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'role', 'bio'
        )


class MeSerializer(BaseUserSerializer):
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

    class Meta:
        """Настройка выдачи."""

        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'role', 'bio'
        )
        read_only_fields = ('role',)
