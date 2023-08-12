# myproject/urls.py

from django.contrib import admin
from django.urls import path, include
from kliniks.views import klinik, klinik_detail

urlpatterns = [
    path("", klinik, name="klinik"),
    path("<int:klinik_id>", klinik_detail, name="klinik"),
]
