from rest_framework import serializers
from django.core.exceptions import FieldError

from .models import User


class GetTokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    def validate(self, data):
        if not User.objects.filter(username=data['username']).exists():
            raise FieldError('Неверное имя пользователя')
        return data


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

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
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'role', 'bio'
        )
