from .views import APIGetToken, APISignUp
from django.urls import path
from django.urls import path

urlpatterns = [
    path('v1/auth/signup', APISignUp.as_view()),
    path('v1/auth/token', APIGetToken.as_view()),
]
