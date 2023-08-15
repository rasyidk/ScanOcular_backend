from rest_framework import serializers
from pemeriksaans.models import Pemeriksaan


class PemeriksaanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pemeriksaan
        fields = "__all__"
