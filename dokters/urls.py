from django.contrib import admin
from django.urls import path, include
from dokters.views import signup2, signin, dokters

urlpatterns = [
    path("signup/", signup2, name="signup"),
    path("signin/", signin, name="signin"),
    path("", dokters, name="dokters"),
]
