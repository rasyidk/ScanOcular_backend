from rest_framework import serializers
from pemeriksaans.models import Pemeriksaan
from pemeriksaans.models import Screening


class PemeriksaanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pemeriksaan
        fields = "__all__"


class ScreeningSerializer(serializers.ModelSerializer):
    class Meta:
        model = Screening
        fields = "__all__"
