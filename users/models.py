from django.db import models


class User(models.Model):
    NIK = models.CharField(max_length=16, unique=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    alamat = models.TextField()
    tanggal_lahir = models.DateField()

    def __str__(self):
        return self.name
