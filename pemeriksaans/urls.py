# myproject/urls.py

from django.contrib import admin
from django.urls import path, include
from pemeriksaans.views import pemeriksaan, pemeriksaan_detail

urlpatterns = [
    path("", pemeriksaan, name="pemeriksaan"),
    path("<int:pemeriksaan_id>", pemeriksaan_detail, name="pemeriksaan"),
]
