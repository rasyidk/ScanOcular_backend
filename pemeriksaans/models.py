from django.db import models

from users.models import User
from relasidokterkliniks.models import Relasidokterklinik


# Create your models here.
class Pemeriksaan(models.Model):
    # dokter = models.ForeignKey(Dokter, on_delete=models.CASCADE, related_name="dokter")
    # klinik = models.ForeignKey(Klinik, on_delete=models.CASCADE, related_name="klinik")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    relasidokterklinik = models.ForeignKey(
        Relasidokterklinik, on_delete=models.CASCADE, related_name="relasidokterklinik"
    )
    bc_id = models.CharField(max_length=255)
    date = models.DateField()
    url_image = models.TextField()