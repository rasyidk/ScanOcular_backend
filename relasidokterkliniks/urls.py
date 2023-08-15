# myproject/urls.py

from django.contrib import admin
from django.urls import path, include
from relasidokterkliniks.views import relasidokterklinik, relasi_detail

urlpatterns = [
    path("relasidokterklinik/", relasidokterklinik, name="klinik"),
    path("relasidokterklinik/<int:relasi_id>", relasi_detail, name="relasi_detail"),
]
