from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from pemeriksaans.serializer import PemeriksaanSerializer
from pemeriksaans.models import Pemeriksaan
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404


# Create your views here.
@api_view(["POST", "GET"])
def pemeriksaan(request):
    if request.method == "POST":
        serializer = PemeriksaanSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            response_data = {
                "message": "pemeriksaan successfully imported",
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "GET":
        return Response("GET", status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST", "GET", "DELETE"])
def pemeriksaan_detail(request, pemeriksaan_id):
    if request.method == "GET":
        try:
            relasi_queryset = Pemeriksaan.objects.select_related("user").get(
                id=pemeriksaan_id
            )

            relasi_data = []
            relasi_info = {
                "user": relasi_queryset.user.name,
                "bc_id": relasi_queryset.bc_id,
            }
            relasi_data.append(relasi_info)
            return Response(relasi_data, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response("doesnt exist", status=status.HTTP_404_NOT_FOUND)

    if request.method == "DELETE":
        try:
            pemeriksaan = get_object_or_404(Pemeriksaan, id=pemeriksaan_id)
            pemeriksaan.delete()
            return Response({"message": "pemeriksaan deleted successfully"})
        except:
            return Response("error", status=status.HTTP_404_NOT_FOUND)
