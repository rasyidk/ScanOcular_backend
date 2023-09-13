from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from pemeriksaans.serializer import PemeriksaanSerializer
from pemeriksaans.serializer import ScreeningSerializer
from pemeriksaans.models import Pemeriksaan
from pemeriksaans.models import Screening
from users.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

from django.core import serializers

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

import smtplib


from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os


def DRsendToEmail(user_id, statusx, penyakit):
    user = get_object_or_404(User, id=user_id)
    smtp_server = "smtp.gmail.com"
    smtp_port = 587  # Use 587 for TLS
    smtp_username = "scanocular@gmail.com"
    smtp_password = "nemkzgrrsfwdfeha"  # You may need an "App Password" if 2-Step Verification is enabled
    msg = MIMEMultipart()
    msg["From"] = "scanocular@gmail.com"
    msg["To"] = user.email
    msg["Subject"] = "Hasil Pemeriksaan SCANOCULAR"
    html_body = """
    <html>
    <head></head>
    <body style="font-family: Arial, sans-serif; background-color: #f4f4f4;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <h1 style="color: #333; text-align: center;">HASIL PEMERIKSAAN SCANOCULAR</h1>
        <p style="font-size: 16px; line-height: 1.6; color: #666;">
            Nama : <b>{nama}</b><br>
            NIK : <b>{nik}</b><br>
            Penyakit : <b>{penyakit}</b><br>
            Hasil Pemeriksaan : <b>{statusx}</b><br>
        </p>
        </div>
    </body>
    </html>
    """
    formatted_html = html_body.format(
        nama=user.name, nik=user.NIK, penyakit=penyakit, statusx=statusx
    )
    msg.attach(MIMEText(formatted_html, "html"))
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
    except Exception as e:
        print(f"Error: {str(e)}")
        exit()

        # Send the email
    try:
        server.sendmail(smtp_username, user.email, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {str(e)}")

        # Close the SMTP server connection
    server.quit()


def sendToEmail(currentTime, user_id, img, diagnosa):
    user = get_object_or_404(User, id=user_id)
    # response_data = {
    #         "id": userget.id,
    #         "name": userget.name,
    #         "nik": userget.NIK,
    #         "email": userget.email,
    #     }

    # Email configuration
    smtp_server = "smtp.gmail.com"
    smtp_port = 587  # Use 587 for TLS
    smtp_username = "scanocular@gmail.com"
    smtp_password = "nemkzgrrsfwdfeha"  # You may need an "App Password" if 2-Step Verification is enabled

    # Create the message object
    msg = MIMEMultipart()

    print("USERRR EMAIL", user.email)
    # Add sender, recipient, subject, and body
    msg["From"] = "scanocular@gmail.com"
    msg["To"] = user.email
    msg["Subject"] = "Hasil Pemeriksaan SCANOCULAR"
    body = "Hello, this is the body of your email."

    html_body = """
    <html>
    <head></head>
    <body style="font-family: Arial, sans-serif; background-color: #f4f4f4;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <h1 style="color: #333; text-align: center;">HASIL PEMERIKSAAN SCANOCULAR</h1>
        <p style="font-size: 16px; line-height: 1.6; color: #666;">
            Tanggal Pemindaian : <b>{currentTime}</b><br>
            Nama : <b>{nama}</b><br>
            NIK : <b>{nik}</b><br>
            Diagnosa : <b>{diagnosa}</b><br>
            Citra :
        </p>
        <p style="font-size: 16px; line-height: 1.6; color: #666;">
        Hasil pemeriksaan akan dikirim ke tenaga ahli pada bidang mata dan akan dilakukan verifikasi apakah diagnosa terkonfirmasi. Informasi terkait hasil verifikasi akan dikirim melalui aplikasi Scanocular.
        </p>
        </div>
    </body>
    </html>
    """

    img_copy = np.ascontiguousarray(img)
    img_base64 = base64.b64encode(img_copy).decode("utf-8")
    formatted_html = html_body.format(
        currentTime=currentTime,
        nama=user.name,
        nik=user.NIK,
        diagnosa=diagnosa,
    )

    msg.attach(MIMEText(formatted_html, "html"))

    file_path = "./Dokumen Hasil Pemeriksaan.pdf"  # Replace with the path to your file
    if os.path.exists(file_path):
        attachment = open(file_path, "rb")
        part = MIMEBase("application", "octet-stream")
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {os.path.basename(file_path)}",
        )
        msg.attach(part)

    # Connect to Gmail's SMTP server, start a TLS connection, and log in
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
    except Exception as e:
        print(f"Error: {str(e)}")
        exit()

    # Send the email
    try:
        server.sendmail(smtp_username, user.email, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {str(e)}")

    # Close the SMTP server connection
    server.quit()


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


def deploysmartcontract(user_id, datetime, img, diagnosa, penyakit):
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
                {"internalType": "string", "name": "_penyakit", "type": "string"},
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
            "inputs": [],
            "name": "penyakit",
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
                {"internalType": "string", "name": "new_penyakit", "type": "string"},
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

    tx_hash = contract.functions.updateMessage(
        user_id, datetime, img, diagnosa, penyakit
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


def getsmartcontract(bc_id):
    web3 = Web3(Web3.HTTPProvider("https://rpc-mumbai.maticvigil.com/"))
    contract_abi = [
        {
            "inputs": [
                {"internalType": "string", "name": "_user_id", "type": "string"},
                {"internalType": "string", "name": "_datetime", "type": "string"},
                {"internalType": "string", "name": "_img", "type": "string"},
                {"internalType": "string", "name": "_diagnosa", "type": "string"},
                {"internalType": "string", "name": "_penyakit", "type": "string"},
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
            "inputs": [],
            "name": "penyakit",
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
                {"internalType": "string", "name": "new_penyakit", "type": "string"},
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

    contract_address = "0x647d314496b374aBB4D3dd819E2a20E0D1859896"  # Replace with your contract's address

    # Replace with your transaction hash
    transaction_hash = bc_id

    try:
        transaction = web3.eth.get_transaction(transaction_hash)
        if transaction:
            input_data = transaction["input"]
            if input_data:
                # Decode input data using the contract ABI
                contract = web3.eth.contract(address=contract_address, abi=contract_abi)
                decoded_input = contract.decode_function_input(input_data)

                print("Decoded Input Data:", decoded_input[1])
                return decoded_input[1]

            else:
                print("Input Data is empty.")
        else:
            print("Transaction not found.")
    except Exception as e:
        print("Error:", str(e))


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

        tx_hash = deploysmartcontract(
            str(user_id), imageName, currentTime, diagnosa, "katarak"
        )

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

        sendToEmail(currentTime, user_id, xx, diagnosa)

        return Response(
            {"diagnosa": diagnosa, "bc_id": tx_hash, "pemeriksaan_id": pemeriksaan_id},
            status=status.HTTP_200_OK,
        )

    else:
        return Response(
            {"message": "crop image not detected"}, status=status.HTTP_410_GONE
        )

    # return Response("res", status=status.HTTP_200_OK)


@api_view(["GET"])
def cekMata_sc(request):
    json_data = json.loads(request.body)
    bc_id = json_data["bc_id"]
    res = getsmartcontract(bc_id)

    return Response(res, status=status.HTTP_200_OK)


@api_view(["GET"])
def pemeriksaan_get_all(request):
    relasi_queryset = Pemeriksaan.objects.select_related("user")
    relasi_data = []

    for relasi in relasi_queryset:
        relasi_info = {
            "id": relasi.id,
            "name": relasi.user.name,
            "email": relasi.user.email,
            "bc_id": relasi.bc_id,
            "date": relasi.date,
            "url_image": relasi.url_image,
            "diagnosa": relasi.diagnosa,
            "penyakit": relasi.penyakit,
            "status": relasi.status,
        }

        relasi_data.append(relasi_info)
        # Use the retrieved fields as needed

    return Response({"data": relasi_data}, status=status.HTTP_200_OK)


@api_view(["POST"])
def cekMata_diabetesretinopati(request):
    try:
        json_data = json.loads(request.body)
        img = json_data["img"]
        # user_id = json_data["user_id"]

        url = "https://classify.roboflow.com/diabetic-retinopathy-screening-ai/1"
        params = {"api_key": "jROYHpfpWHzlprwa48L4"}

        # Define the headers
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        # Make the POST request
        response = requests.post(url, params=params, data=img, headers=headers)
        diagnosa = response.json()["predicted_classes"][0]

        if response.status_code == 200:
            return Response(
                {"diagnosa": diagnosa},
                status=status.HTTP_200_OK,
            )
        else:
            return Response({"message": "error"}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({"message": "not detected"}, status=status.HTTP_404_NOT_FOUND)

    # random_string = generate_random_string(10)

    # # Check for success or error
    # if response.status_code == 200:
    #     imageName = "DR__" + str(user_id) + "__" + str(random_string) + ".jpg"
    #     currentTime = getCurrentTime()
    #     diagnosa = response.json()["predicted_classes"][0]
    #     tx_hash = deploysmartcontract(
    #         str(user_id), currentTime, imageName, diagnosa, "diabetes retinopati"
    #     )
    #     base64ToImg("./media/hasilpemeriksaan/" + imageName + "", img)

    #     pemeriksaan_id = savePemeriksaanToDB(
    #         {
    #             "bc_id": tx_hash,
    #             "date": currentTime,
    #             "url_image": imageName,
    #             "relasidokterklinik": "1",
    #             "user": str(user_id),
    #             "diagnosa": diagnosa,
    #             "penyakit": "diabetes retinopati",
    #         }
    #     )

    #     sendToEmail(currentTime, user_id, "xx", diagnosa)


@api_view(["POST"])
def cekMata_katarak_type2(request):
    json_data = json.loads(request.body)

    img = json_data["img"]
    user_id = json_data["user_id"]

    rf = Roboflow(api_key="jROYHpfpWHzlprwa48L4")
    project = rf.workspace().project("cataractdetection")
    model = project.version(2).model

    imgs = readb64(img)

    # Load the cascade
    # face_cascade = cv2.CascadeClassifier("./alleye.xml")

    # # Detect faces
    # faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    # infer on a local image
    print(model.predict(imgs, confidence=40, overlap=30).json())
    res = model.predict(imgs, confidence=40, overlap=30).json()
    # url = "https://detect.roboflow.com/cataractdetection/2"
    # params = {"api_key": "jROYHpfpWHzlprwa48L4"}
    # headers = {"Content-Type": "application/x-www-form-urlencoded"}
    # response = requests.post(url, params=params, data=img, headers=headers)

    # if response.status_code == 200:
    #     print(response.json())
    # else:
    #     print("Error:", response.text)

    return Response(res, status=status.HTTP_200_OK)


@api_view(["POST", "GET", "DELETE", "PUT"])
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

    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            statusx = data.get("status")
            Pemeriksaan.objects.filter(id=pemeriksaan_id).update(status=statusx)
            return Response({"message": statusx}, status=status.HTTP_200_OK)
        except:
            return Response("error", status=status.HTTP_404_NOT_FOUND)

    if request.method == "DELETE":
        try:
            pemeriksaan = get_object_or_404(Pemeriksaan, id=pemeriksaan_id)
            pemeriksaan.delete()
            return Response({"message": "pemeriksaan deleted successfully"})
        except:
            return Response("error", status=status.HTTP_404_NOT_FOUND)


@api_view(["POST", "GET"])
def screening(request):
    if request.method == "POST":
        serializer = ScreeningSerializer(data=request.data)
        if serializer.is_valid():
            screening = serializer.save()
            screening_id = screening.id
            return Response({"id": screening_id}, status=status.HTTP_200_OK)

    if request.method == "GET":
        relasi_queryset = Screening.objects.select_related("user")
        relasi_data = []
        for relasi in relasi_queryset:
            relasi_info = {
                "id": relasi.id,
                "name": relasi.user.name,
                "email": relasi.user.email,
                "soal_id": relasi.soal_id,
                "value": relasi.value,
                "type_penyakit": relasi.type_penyakit,
                "scan_id": relasi.scan_id,
                "status": relasi.status,
            }

            relasi_data.append(relasi_info)
        #     # Use the retrieved fields as needed

        return Response({"data": relasi_data}, status=status.HTTP_200_OK)


@api_view(["GET", "PUT"])
def screening_detail(request, scan_id):
    if request.method == "GET":
        result_queryset = Screening.objects.filter(scan_id=scan_id)
        relasi_data = []
        for obj in result_queryset:
            print(obj.type_penyakit)
            relasi_info = {
                "id": obj.id,
                "soal_id": obj.soal_id,
                "value": obj.value,
                "type_penyakit": obj.type_penyakit,
                "user_id": obj.user_id,
                "scan_id": obj.scan_id,
                "status": obj.status,
            }
            relasi_data.append(relasi_info)

        if len(relasi_data) == 0:
            return Response(
                {"message": "data not found"}, status=status.HTTP_404_NOT_FOUND
            )
        else:
            return Response({"data": relasi_data}, status=status.HTTP_200_OK)

    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            statusx = data.get("status")

            screenings_before_update = Screening.objects.filter(scan_id=scan_id)
            global user_id
            for i in screenings_before_update:
                user_id = i.user_id
            Screening.objects.filter(scan_id=scan_id).update(status=statusx)

            DRsendToEmail(user_id, statusx, "diabetes retinopati")
            return Response(
                {"message": user_id},
                status=status.HTTP_200_OK,
            )

        except:
            return Response("error", status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
def pemeriksaan_all(request, user_id):
    try:
        relasi_queryset = Pemeriksaan.objects.filter(user=user_id)
        relasi_data = []

        for relasi in relasi_queryset:
            relasi_info = {
                "id": relasi.id,
                "bc_id": relasi.bc_id,
                "date": relasi.date,
                "url_image": relasi.url_image,
                "relasidokterklinik_id": relasi.relasidokterklinik_id,
                "user_id": relasi.user_id,
                "diagnosa": relasi.diagnosa,
                "penyakit": relasi.penyakit,
                "status": relasi.status,
            }
            relasi_data.append(relasi_info)
            # Use the retrieved fields as needed
        if len(relasi_data) == 0:
            return Response("no data", status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"data": relasi_data}, status=status.HTTP_200_OK)
    except:
        Response("error", status=status.HTTP_404_NOT_FOUND)
