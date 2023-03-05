from .views import APIGetToken, APISignUp, APIUser
from django.urls import path, include
from rest_framework.routers import SimpleRouter

router_1 = SimpleRouter(trailing_slash=True)

router_1.register('users', APIUser, basename='user')


urlpatterns = [
    path('', include(router_1.urls)),
    path('auth/signup/', APISignUp.as_view()),
    path('auth/token/', APIGetToken.as_view()),
]
