from views import APIGetToken
from django.urls import path

urlpatterns = [
    path('auth/token/', APIGetToken),
]
