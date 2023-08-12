from django.db import models


class Dokter(models.Model):
    name = models.CharField(max_length=255)
    STR = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    alamat = models.TextField()

    def __str__(self):
        return self.name
