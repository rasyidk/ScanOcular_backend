from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from pemeriksaans.serializer import PemeriksaanSerializer
from pemeriksaans.models import Pemeriksaan
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

import json

import cv2
import base64
import numpy as np
from roboflow import Roboflow
import requests


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
        return Response("GET", status=status.HTTP_200_OK)


def readb64(uri):
    image_array = np.frombuffer(base64.b64decode(uri), np.uint8)
    img = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    return img


@api_view(["POST"])
def cekMata_katarak(request):
    json_data = json.loads(request.body)

    img = readb64(json_data["img"])
    user_id = json_data["user_id"]

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Load the cascade
    face_cascade = cv2.CascadeClassifier("./alleye.xml")

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    global xx
    # Draw rectangle around the faces and crop the faces
    n = 1
    most = {"luas": 0, "faces": 0}
    for x, y, w, h in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        faces = img[y : y + h, x : x + w]
        # cv2.imwrite("face" + str(n) + ".jpg", faces)
        luas = w * h
        if most["luas"] < luas:
            most["luas"] = luas
            xx = faces
            print(n)
        n = n + 1

    cv2.imwrite("matadeteksi.jpg", xx)

    retval, buffer = cv2.imencode(".jpg", img)
    # Convert to base64 encoding and show start of data
    jpg_as_text = base64.b64encode(buffer)
    # print(jpg_as_text)

    rf = Roboflow(api_key="jROYHpfpWHzlprwa48L4")
    project = rf.workspace().project("eye-health3")
    model = project.version(1).model

    print("loading...")
    # infer on a local image
    # print(model.predict(xx, confidence=40, overlap=30).json())
    res = model.predict(xx, confidence=50, overlap=50).json()

    print("selesai")

    return Response(res, status=status.HTTP_200_OK)
    # return Response("res", status=status.HTTP_200_OK)


@api_view(["POST"])
def cekMata_diabetesretinopati(request):
    json_data = json.loads(request.body)
    img = json_data["img"]
    user_id = json_data["user_id"]

    url = "https://classify.roboflow.com/diabetic-retinopathy-screening-ai/1"
    params = {"api_key": "jROYHpfpWHzlprwa48L4"}

    # Define the headers
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    # Make the POST request
    response = requests.post(url, params=params, data=img, headers=headers)

    # Check for success or error
    if response.status_code == 200:
        print(response.json())
    else:
        print("Error:", response.text)

    return Response(response.json(), status=status.HTTP_200_OK)


@api_view(["POST"])
def cekMata_katarak_type2(request):
    json_data = json.loads(request.body)

    img = json_data["img"]
    user_id = json_data["user_id"]

    url = "https://classify.roboflow.com/eye_diseases_detects/1"
    params = {"api_key": "jROYHpfpWHzlprwa48L4"}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(url, params=params, data=img, headers=headers)

    if response.status_code == 200:
        print(response.json())
    else:
        print("Error:", response.text)

    return Response(response.json(), status=status.HTTP_200_OK)


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
