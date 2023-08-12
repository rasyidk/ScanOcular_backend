# users/serializers.py

from rest_framework import serializers
from kliniks.models import Klinik


class KlinikSerializer(serializers.ModelSerializer):
    class Meta:
        model = Klinik
        fields = "__all__"
