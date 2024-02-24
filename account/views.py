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
        if serializer.is_valid() and not VideoflixUser.objects.filter(email=loaded_data['email']).exists():
            serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
            serializer.save()
            return Response({"response": 'user created successfully'}, status=status.HTTP_201_CREATED)
        return Response({"response": 'somthing went wrong'}, status=status.HTTP_400_BAD_REQUEST)


class LoginViewSet(APIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        loaded_data = get_data(request)
        try:
            user = VideoflixUser.objects.get(email=loaded_data['email'])
            if not user.verified:
                return Response({"response": "user is not verified"}, status=status.HTTP_403_FORBIDDEN)
            print(loaded_data['password'])
            print(user.check_password(loaded_data['password']))
            print(user.password)
            if user and user.check_password(loaded_data['password']):
                token, created = Token.objects.get_or_create(user=user)
                return Response({"response": f"{token}"}, status=status.HTTP_201_CREATED)
            else:
                Response({"response": 'login failed'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"response": 'login failed'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"response": 'login failed'}, status=status.HTTP_400_BAD_REQUEST)


class LogoutViewSet(APIView):
    serializer_class = TokenSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        loaded_data = get_data(request)
        try:
            Token.objects.filter(key=loaded_data['token']).delete()
            return Response({'response': 'logout'}, status=status.HTTP_200_OK)
        except:
            return Response({'response': 'failed'}, status=status.HTTP_400_BAD_REQUEST)


class CheckTokenView(APIView):
    serializer_class = TokenSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        return Response({'response': 'verified'}, status=status.HTTP_200_OK)


class CheckVerifyTokenView(APIView):
    serializer_class = TokenSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        loaded_data = get_data(request)
        try:
            user = VideoflixUser.objects.filter(verification_code=loaded_data['token'])
            if user.values('verified')[0]['verified'] == True:
                return Response({'response': 'Du bist bereits verifiziert'}, status=status.HTTP_208_ALREADY_REPORTED)
            elif user.values('verified')[0]['verified'] == False:
                return Response({'response': 'asdasd'}, status=status.HTTP_200_OK)
            return Response({'response': 'Du bist nicht registriert'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'response': 'Du bist nicht registriert'}, status=status.HTTP_400_BAD_REQUEST)


class VerifyUserView(APIView):
    serializer_class = TokenSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        loaded_data = get_data(request)
        user = VideoflixUser.objects.get(verification_code=loaded_data['token'])
        user.verified = True
        user.save()
        return Response({'response': 'ok'}, status=status.HTTP_200_OK)

class SendResetPasswordMail(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        loaded_data = get_data(request)
        print(loaded_data)
        user = VideoflixUser.objects.get(email=loaded_data['email'])
        if user.verified:
            user.create_reset_code()
            send_mail_rest_password(user)
        return Response({'response': f'{user.reset_code}'}, status=status.HTTP_200_OK)

class CheckResetCode(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        loaded_data = get_data(request)
        user = VideoflixUser.objects.get(reset_code=loaded_data['resetcode'])
        if user.exists() & user.verified:
            return Response({'response': True}, status=status.HTTP_200_OK)
        else:
            return Response({'response': False}, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        loaded_data = get_data(request)
        user = VideoflixUser.objects.get(reset_code=loaded_data['resetcode'])
        if user.exists() & user.verified:
            user.password = make_password(loaded_data['password'])
            user.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)