from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework import status, views
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from projects.models import Project
from usermanagement.models import User, UserProfile
from usermanagement.serializers import LoginSerializer
from drf_yasg import openapi
from usermanagement.firebase import firebase_app
from knox.models import AuthToken
from firebase_admin import auth
from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes
from knox.settings import CONSTANTS


class LoginView(views.APIView):
    @swagger_auto_schema(
        operation_description="Login to the app",
        request_body=LoginSerializer,
        responses={
            status.HTTP_200_OK: "Success",
        },
        security=[],
    )
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(email=email, password=password)
        if user:
            return Response({"token": user.auth_token.key})
        else:
            return Response(
                {"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST
            )


class FirebaseLoginView(views.APIView):
    """
    Use this endpoint to login or register a user with a Firebase token.
    """

    @swagger_auto_schema(
        operation_description="Firebase login",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "id_token": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Firebase ID token"
                )
            },
            required=["id_token"],
        ),
        responses={200: "OK", 400: "Bad Request", 500: "Internal Server Error"},
    )
    def post(self, request):
        id_token = request.data.get("id_token")
        try:
            decoded_token = auth.verify_id_token(id_token)
            print("decoded_token", decoded_token)
            uid = decoded_token["uid"]
            email = decoded_token["email"]
            user, created = User.objects.get_or_create(email=email, username=email)

            if created:
                user.email = email
                user.username = email

                user.uid = uid
                user.first_name = decoded_token.get("name") or email.split("@")[0]
                user.save()

                user_profile = UserProfile.objects.create(
                    user=user, image=decoded_token.get("picture"), coins=0
                )
                user_profile.save()
            else:
                print("user already exists")
                user_profile, created = UserProfile.objects.get_or_create(user=user)
                if created:
                    user_profile.coins = 0
                    user_profile.image = decoded_token.get("picture")
                    user_profile.save()

            # Generate Django token
            token_instance, token = AuthToken.objects.create(user=user)
            print("token_instance", token)

            return Response(
                {
                    "user": {
                        "id": uid,
                        "email": user.email,
                        "name": user.first_name,
                        "coins": user_profile.coins,
                        "photoUrl": user_profile.image,
                    },
                    "token": token,
                }
            )
        except ValueError as e:
            print(e)
            return Response({"error": str(e)}, status=400)


class FirebaseLogoutView(views.APIView):
    """
    Use this endpoint to logout a user.
    """

    @swagger_auto_schema(
        operation_description="Firebase logout",
        responses={200: "OK", 400: "Bad Request", 500: "Internal Server Error"},
    )
    def post(self, request):
        authentication_classes = [TokenAuthentication]
        permission_classes = [IsAuthenticated]
        print("request.headers", request.headers)
        id_token = request.headers.get("Authorization").split(" ")[1]
        print("id_token", id_token)
        try:
            decoded_token = auth.verify_id_token(id_token)
            uid = decoded_token["uid"]

            user = User.objects.get(uid=uid)

            # Delete Django token
            AuthToken.objects.filter(user=user).delete()

            return Response({"detail": "Logout successful"})
        except ValueError as e:
            print(e)
            return Response({"detail": str(e)}, status=400)


class UserView(views.APIView):
    @swagger_auto_schema(
        operation_description="Get user details",
        responses={
            status.HTTP_200_OK: "Success",
        },
    )
    def get(self, request):
        print("request.headers", request.headers)
        authentication_classes = [TokenAuthentication]
        permission_classes = [IsAuthenticated]
        knox_token = request.headers.get("Authorization").split(" ")[1]

        uid = AuthToken.objects.get(
            token_key=knox_token[: CONSTANTS.TOKEN_KEY_LENGTH]
        ).user.uid

        user = User.objects.get(uid=uid)
        user_profile = UserProfile.objects.get(user=user)
        projects = Project.objects.filter(participants=user_profile)

        return Response(
            {
                "id": user.uid,
                "email": user.email,
                "name": user.first_name,
                "coins": user_profile.calculated_coins,
                "photo_url": user_profile.image,
            }
        )

    @swagger_auto_schema(
        operation_description="Delete user account",
        responses={
            status.HTTP_200_OK: "Success",
        },
    )
    def delete(self, request):
        print("request.headers", request.headers)
        authentication_classes = [TokenAuthentication]
        permission_classes = [IsAuthenticated]
        knox_token = request.headers.get("Authorization").split(" ")[1]

        uid = AuthToken.objects.get(
            token_key=knox_token[: CONSTANTS.TOKEN_KEY_LENGTH]
        ).user.uid

        user = User.objects.get(uid=uid)
        user_profile = UserProfile.objects.get(user=user)
        user.delete()
        user_profile.delete()

        return Response(
            {
                "detail": "Account deleted",
            }
        )
