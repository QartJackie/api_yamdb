from rest_framework import serializers
from django.core.exceptions import FieldError

from .models import User


class GetTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50, required=True)
    confirmation_code = serializers.CharField(required=True)

    def validate(self, username):
        if not User.objects.filter(username=username).exists():
            raise FieldError('Неверное имя пользователя')
        return username
