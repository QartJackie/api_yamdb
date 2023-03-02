from .views import APIGetToken, APISignUp, APIUser
from django.urls import path, include
from rest_framework.routers import SimpleRouter

v1_router = SimpleRouter(trailing_slash=False)

v1_router.register('users', APIUser, basename='user')

urlpatterns = [
    path('', include(v1_router.urls)),
    path('v1/auth/signup', APISignUp.as_view()),
    path('v1/auth/token', APIGetToken.as_view()),
]
