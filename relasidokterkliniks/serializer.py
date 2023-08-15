from rest_framework import serializers
from .models import Relasidokterklinik


class RelasidokterklinikSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relasidokterklinik
        fields = "__all__"
