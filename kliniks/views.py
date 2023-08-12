from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from kliniks.serializer import KlinikSerializer
from .models import Klinik
from django.shortcuts import get_object_or_404


@api_view(["POST"])
def klinik(request):
    serializer = KlinikSerializer(data=request.data)
    if serializer.is_valid():
        klinik = serializer.save()

        # Customize the data you want to return
        response_data = {
            "message": "Klinik registered successfully",
            "id": klinik.id,
            "nama_klinik": klinik.nama_klinik,
            "alamat": klinik.alamat,
            "kode_pos": klinik.kode_pos,
            # Add more fields as needed
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "DELETE"])
def klinik_detail(request, klinik_id):
    if request.method == "GET":
        klinik = get_object_or_404(Klinik, id=klinik_id)
        response_data = {
            "id": klinik.id,
            "name": klinik.nama_klinik,
            # Add more fields as needed
        }
        return Response(response_data)

    elif request.method == "DELETE":
        klinik = get_object_or_404(Klinik, id=klinik_id)
        klinik.delete()
        return Response({"message": "Klinik deleted successfully"})


# @api_view(["DELETE"])
# def klinik_delete(request, klinik_id):
#     klinik = get_object_or_404(Klinik, id=klinik_id)
#     # Perform actions with the klinik object, such as retrieving details
#     # Customize the data you want to return in the JSON response
#     klinik.delete()
#     return Response({"message": "Klinik deleted successfully"})


# @api_view(["DELETE"])
# def klinik(request):
#     return Response("POST", status=status.HTTP_400_BAD_REQUEST)
