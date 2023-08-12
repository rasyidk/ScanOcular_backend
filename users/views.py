# users/views.py

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import UserSerializer
from django.contrib.auth import authenticate
from .models import User
from django.contrib.auth.hashers import check_password
import bcrypt


@api_view(["POST"])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()

        # Hash the password using bcrypt
        password = request.data.get("password")
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        # Update the user's password with the hashed password
        user.password = hashed_password.decode("utf-8")
        user.save()

        # Customize the data you want to return
        response_data = {
            "message": "User registered successfully",
            "user_id": user.id,
            "name": user.name,
            "email": user.email,
            # Add more fields as needed
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def signin(request):
    email = request.data.get("email")
    password = request.data.get("password")

    try:
        user = User.objects.get(email=email)
        hashed_password = user.password.encode("utf-8")

        if bcrypt.checkpw(password.encode("utf-8"), hashed_password):
            return Response({"message": "Sign-in successful!"})
        else:
            return Response(
                {"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )
    except User.DoesNotExist:
        return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
