from rest_framework import viewsets, permissions, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

from account.models import VideoflixUser
from account.serializers import RegistrationSerializer, LoginSerializer, LogoutSerializer


# Create your views here.

class RegistrationViewSet(APIView):
    queryset = VideoflixUser.objects.none()
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            loadedData = json.loads(request.body)
        except:
            requestData = request.data
            loadedData = json.loads(json.dumps(requestData.dict()))
        serializer = RegistrationSerializer(data=loadedData)
        if serializer.is_valid() and not VideoflixUser.objects.filter(email=loadedData['email']).exists():
            serializer.save()
            return Response({"response": 'user created successfully'}, status=status.HTTP_201_CREATED)
        return Response({"response": 'somthing went wrong'}, status=status.HTTP_400_BAD_REQUEST)

class LoginViewSet(APIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            loadedData = json.loads(request.body)
        except:
            requestData = request.data
            loadedData = json.loads(json.dumps(requestData.dict()))
        try:
            user = VideoflixUser.objects.get(email=loadedData['email'])
            if user and user.check_password(loadedData['password']):
                token, created = Token.objects.get_or_create(user=user)
                return Response({"response": f"{token}"}, status=status.HTTP_200_OK)
            else:
                Response({"response": 'login failed'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"response": 'login failed'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"response": 'login failed'}, status=status.HTTP_400_BAD_REQUEST)

class LogoutViewSet(APIView):
    serializer_class = LogoutSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        try:
            loadedData = json.loads(request.body)
        except:
            requestData = request.data
            loadedData = json.loads(json.dumps(requestData.dict()))
        try:
            Token.objects.filter(key=loadedData['token']).delete()
            return Response({'response': 'logout'}, status=status.HTTP_200_OK)
        except:
            return Response({'response': 'failed'}, status=status.HTTP_400_BAD_REQUEST)