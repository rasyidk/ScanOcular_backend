from django.shortcuts import render

from dokters.models import Dokter
from kliniks.models import Klinik
from relasidokterkliniks.models import Relasidokterklinik
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializer import RelasidokterklinikSerializer
from django.shortcuts import get_object_or_404


# Create your views here.
@api_view(["GET", "POST"])
def relasidokterklinik(request):
    if request.method == "GET":
        relasi_queryset = Relasidokterklinik.objects.select_related("dokter", "klinik")
        relasi_data = []

        for relasi in relasi_queryset:
            dokter_name = relasi.dokter.name
            klinik_nama = relasi.klinik.nama_klinik

            relasi_info = {
                "dokter_name": dokter_name,
                "nama_klinik": klinik_nama,
            }
            relasi_data.append(relasi_info)
            # Use the retrieved fields as needed

        return Response(relasi_data, status=status.HTTP_201_CREATED)

    if request.method == "POST":
        serializer = RelasidokterklinikSerializer(data=request.data)
        if serializer.is_valid():
            relasi = serializer.save()
            response_data = {
                "message": "Relasi registered successfully",
                "dokter_id": relasi.dokter_id,
                "klinik_id": relasi.klinik_id
                # Add more fields as needed
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
def relasi_detail(request, relasi_id):
    relasi = get_object_or_404(Klinik, id=relasi_id)
    relasi.delete()

    return Response({"message": "Klinik deleted successfully"})
