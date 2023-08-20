# myproject/urls.py

from django.contrib import admin
from django.urls import path, include
from users.views import signup, signin

urlpatterns = [
    path("signup/", signup, name="signup"),
    path("signin/", signin, name="signin"),
]
