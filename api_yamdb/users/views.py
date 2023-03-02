from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.filters import SearchFilter

from .models import User
from .serializers import GetTokenSerializer, UserSerializer, UserSearchSerializer


def send_email(email, username):
    user = get_object_or_404(User, username=username)
    conf_code = user.confirmation_code
    send_mail(
        subject='Код подтверждения',
        message=f'Ваш код {conf_code}',
        from_email=0,
        recipient_list=[email]
    )


class APIGetToken(APIView):
    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = request.data.get('username')
        confirmation_code = request.data.get('confirmation_code')
        user = get_object_or_404(
            User,
            username=username,
        )
        print(serializer.data)
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
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
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
#    permission_classes = только админ
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter,)
    search_fields = ('username') 

    def perform_create(self, serializer):
        serializer.save(username=serializer.validated_data['username'], email=serializer.validated_data['email'])



    
