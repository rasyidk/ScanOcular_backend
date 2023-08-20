from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/users/", include("users.urls")),
    path("api/users/dokter/", include("dokters.urls")),
    path("api/klinik/", include("kliniks.urls")),
    path("api/relasi/", include("relasidokterkliniks.urls")),
    path("api/pemeriksaan/", include("pemeriksaans.urls")),
    path("", include("example.urls")),
]
