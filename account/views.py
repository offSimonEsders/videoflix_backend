from rest_framework import viewsets, permissions, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

from account.models import VideoflixUser
from account.serializers import RegistrationSerializer, LoginSerializer, TokenSerializer


# Create your views here.

class RegistrationViewSet(APIView):
    queryset = VideoflixUser.objects.none()
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            loaded_data = json.loads(request.body)
        except:
            request_data = request.data
            loaded_data = json.loads(json.dumps(request_data.dict()))
        serializer = RegistrationSerializer(data=loaded_data)
        if serializer.is_valid() and not VideoflixUser.objects.filter(email=loaded_data['email']).exists():
            serializer.save()
            return Response({"response": 'user created successfully'}, status=status.HTTP_201_CREATED)
        return Response({"response": 'somthing went wrong'}, status=status.HTTP_400_BAD_REQUEST)

class LoginViewSet(APIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            loaded_data = json.loads(request.body)
        except:
            request_data = request.data
            loaded_data = json.loads(json.dumps(request_data.dict()))
        try:
            user = VideoflixUser.objects.get(email=loaded_data['email'])
            if not user.verified:
                return Response({"response": "user is not verified"}, status=status.HTTP_403_FORBIDDEN)
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
        try:
            loaded_data = json.loads(request.body)
        except:
            request_data = request.data
            loaded_data = json.loads(json.dumps(request_data.dict()))
        try:
            Token.objects.filter(key=loaded_data['token']).delete()
            return Response({'response': 'logout'}, status=status.HTTP_200_OK)
        except:
            return Response({'response': 'failed'}, status=status.HTTP_400_BAD_REQUEST)

class CheckTokenView(APIView):
    serializer_class = TokenSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        return Response({'response': 'verified'}, status=status.HTTP_200_OK)