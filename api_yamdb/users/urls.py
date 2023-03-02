from .views import APIGetToken, APISignUp, APIUser, APIMe
from django.urls import path, include
from rest_framework.routers import SimpleRouter

v1_router = SimpleRouter(trailing_slash=False)

v1_router.register('users', APIUser, basename='user')
v1_router.register('me', APIMe, basename='me')


urlpatterns = [
    path('', include(v1_router.urls)),
    path('auth/signup', APISignUp.as_view()),
    path('auth/token', APIGetToken.as_view()),
]
