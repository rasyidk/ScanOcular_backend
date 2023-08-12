from django.db import models


# Create your models here.
class Klinik(models.Model):
    nama_klinik = models.CharField(max_length=16)
    kode_pos = models.CharField(max_length=255)
    alamat = models.TextField()

    def __str__(self):
        return self.name
