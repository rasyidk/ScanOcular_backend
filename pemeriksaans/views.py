from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from pemeriksaans.serializer import PemeriksaanSerializer
from pemeriksaans.models import Pemeriksaan
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

import json
import base64
from PIL import Image
from io import BytesIO
import cv2
import base64
import numpy as np
from roboflow import Roboflow
import requests

import random
import string
import datetime
import pytz

from web3 import Web3, Account


def getCurrentTime():
    timezone = pytz.timezone("Asia/Bangkok")

    # Get the current UTC time
    utc_now = datetime.datetime.utcnow()

    # Convert UTC time to GMT+7 (Indochina Time)
    ict_now = utc_now.replace(tzinfo=pytz.utc).astimezone(timezone)

    # Format the datetime as a string
    current_time_in_ict = ict_now.strftime("%Y-%m-%d %H:%M")

    return current_time_in_ict


def base64ToImg(imgname, data):
    image_data = data

    # Decode the base64 data
    image_bytes = base64.b64decode(image_data)

    # Create a BytesIO object to work with the image data
    image_buffer = BytesIO(image_bytes)

    # Open the image using PIL (Python Imaging Library)
    img = Image.open(image_buffer)

    # Save the image to a file
    img.save(imgname)


def deploysmartcontract(user_id, datetime, img, diagnosa):
    polygon_rpc_url = "https://rpc-mumbai.maticvigil.com/"
    contract_address = "0x647d314496b374aBB4D3dd819E2a20E0D1859896"  # Replace with your contract's address
    private_key = "db7038c44c183593323f3ae779d8559248dc5ec77a2a79b72ef0d6aba8a70620"  # Replace with your private key

    # Initialize a Web3 connection
    web3 = Web3(Web3.HTTPProvider(polygon_rpc_url))

    # Load your contract ABI and address
    contract_abi = [
        {
            "inputs": [
                {"internalType": "string", "name": "_user_id", "type": "string"},
                {"internalType": "string", "name": "_datetime", "type": "string"},
                {"internalType": "string", "name": "_img", "type": "string"},
                {"internalType": "string", "name": "_diagnosa", "type": "string"},
            ],
            "stateMutability": "nonpayable",
            "type": "constructor",
        },
        {
            "inputs": [],
            "name": "datetime",
            "outputs": [{"internalType": "string", "name": "", "type": "string"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "diagnosa",
            "outputs": [{"internalType": "string", "name": "", "type": "string"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "img",
            "outputs": [{"internalType": "string", "name": "", "type": "string"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "string", "name": "new_user_id", "type": "string"},
                {"internalType": "string", "name": "new_datetime", "type": "string"},
                {"internalType": "string", "name": "new_img", "type": "string"},
                {"internalType": "string", "name": "new_diagnosa", "type": "string"},
            ],
            "name": "updateMessage",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "user_id",
            "outputs": [{"internalType": "string", "name": "", "type": "string"}],
            "stateMutability": "view",
            "type": "function",
        },
    ]
    # Replace with your contract's ABI
    contract = web3.eth.contract(address=contract_address, abi=contract_abi)

    # Set the sender's account using your private key (be careful with private keys)
    sender_account = Account.from_key(private_key)

    new_message = "Hello, Python and Polygon!"
    tx_hash = contract.functions.updateMessage(
        user_id, datetime, img, diagnosa
    ).build_transaction(
        {
            "chainId": 80001,  # Mumbai Testnet chain ID
            "gas": 100000,  # Adjust gas limit as needed
            "gasPrice": web3.to_wei("10", "gwei"),
            "nonce": web3.eth.get_transaction_count(sender_account.address),
        }
    )

    signed_tx = web3.eth.account.sign_transaction(tx_hash, private_key)
    tx_receipt = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print("Transaction Hash:", tx_receipt.hex())

    return tx_receipt.hex()


def savePemeriksaanToDB(datax):
    serializer = PemeriksaanSerializer(data=datax)
    if serializer.is_valid():
        pemeriksaan = serializer.save()
        pemeriksaan_id = pemeriksaan.id
        return pemeriksaan_id


def generate_random_string(length):
    characters = (
        string.ascii_letters + string.digits
    )  # You can include additional characters if needed
    return "".join(random.choice(characters) for _ in range(length))


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
    xx = None
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

    if xx is not None:
        random_string = generate_random_string(10)

        rf = Roboflow(api_key="jROYHpfpWHzlprwa48L4")
        project = rf.workspace().project("eye-health3")
        model = project.version(1).model

        print("loading...")
        # infer on a local image
        # print(model.predict(xx, confidence=40, overlap=30).json())
        res = model.predict(xx, confidence=50, overlap=50).json()

        print("selesai")

        print("print image")

        imageName = "" + str(user_id) + "__" + str(random_string) + ".jpg"
        currentTime = getCurrentTime()
        diagnosa = res["predictions"][0]["class"]

        tx_hash = deploysmartcontract(str(user_id), imageName, currentTime, diagnosa)

        cv2.imwrite(
            "./media/hasilpemeriksaan/" + imageName + "",
            xx,
        )

        # savePemeriksaanToDB(
        #     {
        #         "bc_id": {tx_hash},
        #         "date": {currentTime},
        #         "url_image": {imageName},
        #         "relasidokterklinik": "1",
        #         "user": {str(user_id)},
        #     }
        # )

        pemeriksaan_id = savePemeriksaanToDB(
            {
                "bc_id": tx_hash,
                "date": currentTime,
                "url_image": imageName,
                "relasidokterklinik": "1",
                "user": str(user_id),
                "diagnosa": diagnosa,
                "penyakit": "katarak",
            }
        )

        return Response(
            {"diagnosa": diagnosa, "bc_id": tx_hash, "pemeriksaan_id": pemeriksaan_id},
            status=status.HTTP_200_OK,
        )

    else:
        return Response(
            {"message": "crop image not detected"}, status=status.HTTP_410_GONE
        )

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

    random_string = generate_random_string(10)

    # Check for success or error
    if response.status_code == 200:
        imageName = "DR__" + str(user_id) + "__" + str(random_string) + ".jpg"
        currentTime = getCurrentTime()
        diagnosa = response.json()["predicted_classes"][0]
        tx_hash = deploysmartcontract(str(user_id), imageName, currentTime, diagnosa)
        base64ToImg("./media/hasilpemeriksaan/" + imageName + "", img)

        pemeriksaan_id = savePemeriksaanToDB(
            {
                "bc_id": tx_hash,
                "date": currentTime,
                "url_image": imageName,
                "relasidokterklinik": "1",
                "user": str(user_id),
                "diagnosa": diagnosa,
                "penyakit": "diabetes retinopati",
            }
        )

        return Response(
            {"diagnosa": diagnosa, "bc_id": tx_hash, "pemeriksaan_id": pemeriksaan_id},
            status=status.HTTP_200_OK,
        )
    else:
        print("Error:", response.text)


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
