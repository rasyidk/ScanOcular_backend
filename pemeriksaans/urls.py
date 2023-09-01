# myproject/urls.py

from django.contrib import admin
from django.urls import path, include
from pemeriksaans.views import (
    pemeriksaan,
    pemeriksaan_detail,
    cekMata,
    cekMata_diabetesretinopati,
)

urlpatterns = [
    path("", pemeriksaan, name="pemeriksaan"),
    path("cekmata/katarak", cekMata, name="pemeriksaan"),
    path("cekmata/dr", cekMata_diabetesretinopati, name="cekMata_diabetesretinopati"),
    path("<int:pemeriksaan_id>", pemeriksaan_detail, name="pemeriksaan"),
]
