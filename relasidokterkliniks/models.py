from django.db import models
from dokters.models import Dokter
from kliniks.models import Klinik


# Create your models here.
class Relasidokterklinik(models.Model):
    dokter = models.ForeignKey(Dokter, on_delete=models.CASCADE, related_name="dokter")
    klinik = models.ForeignKey(Klinik, on_delete=models.CASCADE, related_name="klinik")

    def __str__(self):
        return self.name
