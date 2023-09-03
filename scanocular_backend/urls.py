from django.contrib import admin
from django.urls import path, include


from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/users/", include("users.urls")),
    path("api/users/dokter/", include("dokters.urls")),
    path("api/klinik/", include("kliniks.urls")),
    path("api/relasi/", include("relasidokterkliniks.urls")),
    path("api/pemeriksaan/", include("pemeriksaans.urls")),
    path("", include("example.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
