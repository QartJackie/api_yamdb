from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail

from .permissions import IsAdmin, IsAuthorOrReadOnly
from .models import User
from .serializers import (
    GetTokenSerializer, UserSerializer, UserSearchSerializer
)


class EnablePartialUpdateMixin:
    def patch(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


def send_email(email, username):
    user = get_object_or_404(User, username=username)
    conf_code = user.confirmation_code
    send_mail(
        subject='Код подтверждения',
        message=f'Ваш код {conf_code}',
        from_email="admin@yamdb.com",
        recipient_list=[email]
    )


class APIGetToken(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = request.data.get('username')
        confirmation_code = request.data.get('confirmation_code')
        user = get_object_or_404(
            User,
            username=username,
        )
        if not User.objects.filter(username=username).exists():
            return Response(
                'Пользователь с таким именем не существует',
                status=status.HTTP_404_NOT_FOUND
            )
        if user.confirmation_code != confirmation_code:
            return Response(
                'Неверный код',
                status=status.HTTP_400_BAD_REQUEST)
        refresh = RefreshToken.for_user(user)
        return Response(
            {'access_token': str(refresh.access_token)},
            status=status.HTTP_200_OK
        )


class APISignUp(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            if User.objects.filter(
                email=request.data['email'], username=request.data['username']
            ).exists():
                return Response(status=status.HTTP_200_OK)
            elif User.objects.filter(email=request.data['email']).exists():
                return Response(status=status.HTTP_400_BAD_REQUEST)
            elif User.objects.filter(
                username=request.data['username']
            ).exists():
                return Response(status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            send_email(serializer.data['email'], serializer.data['username'])
            return Response(
                {
                    'email': serializer.data['email'],
                    'username': serializer.data['username']
                },
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APIUser(viewsets.ModelViewSet):
    queryset = User.objects.all()
    lookup_field = 'username'
    serializer_class = UserSearchSerializer
    permission_classes = (IsAdmin,)
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter,)
    search_fields = ('username')

    def perform_create(self, serializer):
        username = serializer.validated_data.get('username')
        if '|' in username:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer.save()


class APIMe(EnablePartialUpdateMixin, viewsets.ModelViewSet):
    serializer_class = UserSearchSerializer
    lookup_field = 'username'
    queryset = User.objects.all()
    permission_classes = (IsAuthorOrReadOnly,)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = queryset.get(username=self.request.user.username)
        return obj
