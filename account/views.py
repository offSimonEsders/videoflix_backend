from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.views import APIView

from account.models import VideoflixUser
from account.serializers import UserSerializer


# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = VideoflixUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]