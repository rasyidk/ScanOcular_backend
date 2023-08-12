# users/serializers.py

from rest_framework import serializers
from .models import Dokter


class DokterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dokter
        fields = "__all__"
