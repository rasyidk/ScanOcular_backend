# myproject/urls.py

from django.contrib import admin
from django.urls import path, include
from pemeriksaans.views import (
    pemeriksaan,
    pemeriksaan_detail,
    cekMata_katarak,
    cekMata_katarak_type2,
    cekMata_diabetesretinopati,
    cekMata_sc,
    screening,
    screening_detail,
    pemeriksaan_all,
)

urlpatterns = [
    path("", pemeriksaan, name="pemeriksaan"),
    path("cekmata/katarak", cekMata_katarak, name="cekMata1"),
    path("cekmata/katarak2", cekMata_katarak_type2, name="cekMata2"),
    path("cekmata/dr", cekMata_diabetesretinopati, name="cekMata_diabetesretinopati"),
    path("cekmata/sc", cekMata_sc, name="getsmartcontract"),
    path("cekmata/screening", screening, name="screening"),
    path("cekmata/screening/<str:scan_id>", screening_detail, name="screeningx"),
    # path("user/all", pemeriksaan_get_all, name="pemeriksaan"),
    path("user/<int:user_id>", pemeriksaan_all, name="pemeriksaan all"),
    path("<int:pemeriksaan_id>", pemeriksaan_detail, name="pemeriksaan"),
]
