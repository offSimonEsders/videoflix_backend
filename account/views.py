from django.contrib.auth.hashers import make_password
from rest_framework import viewsets, permissions, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .signals import send_mail_rest_password

from account.models import VideoflixUser
from account.serializers import RegistrationSerializer, LoginSerializer, TokenSerializer
from account.utils import get_data


# Create your views here.

class RegistrationViewSet(APIView):
    queryset = VideoflixUser.objects.none()
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        loaded_data = get_data(request)
        serializer = RegistrationSerializer(data=loaded_data)
        if serializer.is_valid():
            if not VideoflixUser.objects.filter(email=serializer.validated_data['email']).exists():
                serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
                serializer.save()
                return Response({"response": 'Nutzer erfolgreich erstellt'}, status=status.HTTP_201_CREATED)
        return Response({"response": 'Etwas ist schiefgelaufen'}, status=status.HTTP_400_BAD_REQUEST)


class LoginViewSet(APIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        loaded_data = get_data(request)
        serializer = LoginSerializer(data=loaded_data)
        if not serializer.is_valid():
            return Response({"response": 'Login fehlgeschlagen'}, status=status.HTTP_400_BAD_REQUEST)
        user = VideoflixUser.objects.get(email=serializer.validated_data['email'])
        if not user.verified:
            return Response({"response": "Du bist nicht verifiziert"}, status=status.HTTP_403_FORBIDDEN)
        elif user and user.check_password(serializer.validated_data['password']):
            token, created = Token.objects.get_or_create(user=user)
            return Response({"response": f"{token}"}, status=status.HTTP_201_CREATED)
        else:
            Response({"response": 'Login fehlgeschlagen'}, status=status.HTTP_400_BAD_REQUEST)


class LogoutViewSet(APIView):
    serializer_class = TokenSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        loaded_data = get_data(request)
        serializer = TokenSerializer(data=loaded_data)
        if serializer.is_valid():
            Token.objects.filter(key=serializer.validated_data['token']).delete()
            return Response({'response': 'Ausgeloggt'}, status=status.HTTP_200_OK)
        else:
            return Response({'response': 'Fehlgeschlagen'}, status=status.HTTP_400_BAD_REQUEST)


class CheckTokenView(APIView):
    serializer_class = TokenSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        return Response({'response': 'Verifiziert'}, status=status.HTTP_200_OK)


class CheckVerifyTokenView(APIView):
    serializer_class = TokenSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        loaded_data = get_data(request)
        serializer = TokenSerializer(data=loaded_data)
        try:
            if not serializer.is_valid():
                return Response({'response': 'Deine Anfrage ist nicht gültig'}, status=status.HTTP_400_BAD_REQUEST)
            user = VideoflixUser.objects.filter(verification_code=serializer.validated_data['token'])
            if user.values('verified')[0]['verified'] == True:
                return Response({'response': 'Du bist bereits verifiziert'}, status=status.HTTP_208_ALREADY_REPORTED)
            elif user.values('verified')[0]['verified'] == False:
                return Response({'response': 'ok'}, status=status.HTTP_200_OK)
            return Response({'response': 'Du bist nicht registriert'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'response': 'Du bist nicht registriert'}, status=status.HTTP_400_BAD_REQUEST)


class VerifyUserView(APIView):
    serializer_class = TokenSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        loaded_data = get_data(request)
        serializer = TokenSerializer(data=loaded_data)
        if serializer.is_valid():
            user = VideoflixUser.objects.get(verification_code=serializer.validated_data['token'])
            user.verified = True
            user.save()
            return Response({'response': 'ok'}, status=status.HTTP_200_OK)
        else:
            return Response({'response': 'false'}, status=status.HTTP_400_BAD_REQUEST)


class SendResetPasswordMail(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        loaded_data = get_data(request)
        try:
            user = VideoflixUser.objects.get(email=loaded_data['email'])
            if user.verified:
                user.create_reset_code()
                send_mail_rest_password(user)
            return Response({'response': 'ok'}, status=status.HTTP_200_OK)
        except:
            return Response({'response': 'false'}, status=status.HTTP_400_BAD_REQUEST)


class CheckResetCode(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        loaded_data = get_data(request)
        serializer = TokenSerializer(data=loaded_data)
        if serializer.is_valid():
            user = VideoflixUser.objects.get(reset_code=serializer.validated_data['token'])
            if user and user.verified:
                return Response({'response': 'true'}, status=status.HTTP_200_OK)
            else:
                return Response({'response': 'false'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'response': 'false'}, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        loaded_data = get_data(request)
        serializer = TokenSerializer(data=loaded_data)
        if serializer.is_valid():
            user = VideoflixUser.objects.get(reset_code=loaded_data['token'])
            if user and user.verified and len(loaded_data['token']) > 30 and len(loaded_data['password']) >= 8:
                user.password = make_password(loaded_data['password'])
                user.reset_code = ''
                user.save()
                return Response({'response': 'Passwort geändert'}, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
