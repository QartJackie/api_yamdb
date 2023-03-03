from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.core.exceptions import ValidationError

from .models import User


class GetTokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)


class UserSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=254)
    username = serializers.SlugField(required=True, max_length=150)

    def validate(self, validated_data):
        if validated_data['username'] == 'me':
            raise ValidationError('Данное имя недоступно')
        return validated_data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email']
        )
        return user

    class Meta:
        model = User
        fields = ('email', 'username')


class UserSearchSerializer(serializers.ModelSerializer):

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
        if validated_data['username'] == 'me':
            raise ValidationError('Данное имя недоступно')
        return validated_data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email']
        )
        return user

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'role', 'bio'
        )
