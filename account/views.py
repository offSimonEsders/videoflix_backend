from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from rest_framework import viewsets, permissions, status
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView

from account.models import VideoflixUser
from account.serializers import UserSerializer


# Create your views here.

class UserViewSet(APIView):
    queryset = VideoflixUser.objects.none()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            data = json.loads(request.body)
        except:
            dictd = request.data
            data = json.loads(json.dumps(dictd.dict()))
        serializer = UserSerializer(data=data)
        if serializer.is_valid() and not VideoflixUser.objects.filter(email=data['email']).exists():
            serializer.save()
            return Response("user created succesfully", status=status.HTTP_201_CREATED)
        return Response("somthing went wrong", status=status.HTTP_400_BAD_REQUEST)