from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail

from .permissions import IsAdmin
from .models import User
from .serializers import (
    GetTokenSerializer, UserSerializer, UserSearchSerializer, MeSerializer
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
        username = serializer.data.get('username')
        confirmation_code = serializer.data.get('confirmation_code')
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
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        username = serializer.validated_data.get('username')
        if User.objects.get_or_create(
            email=email, username=username
        ):
            send_email(
                email=email,
                username=username
            )
            return Response(
                {
                    'email': email,
                    'username': username
                }, status=status.HTTP_200_OK
            )


class APIUser(viewsets.ModelViewSet):
    queryset = User.objects.all()
    lookup_field = 'username'
    serializer_class = UserSearchSerializer
    permission_classes = (IsAdmin,)
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def perform_create(self, serializer):
        serializer.save()
        return serializer.data

    @action(
        methods=[
            "get",
            "patch",
        ],
        detail=False,
        url_path="me",
        permission_classes=(IsAuthenticated,),
        serializer_class=MeSerializer,
    )
    def users_own_profile(self, request):
        user = request.user
        if request.method == "GET":
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == "PATCH":
            serializer = self.get_serializer(
                user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
