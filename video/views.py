from django.shortcuts import render
from django.views.static import serve
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from video.models import Video
from video.serializers import VideoSerializer
from videoflix_backend import settings


# Create your views here.

class VideoView(APIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAuthenticated]


    def get(self, request):
        serializer = VideoSerializer(Video.objects.all(), many=True)
        return Response(data=serializer.data)

class MediaView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, path):
        document_root = settings.MEDIA_ROOT
        return serve(request, document_root=document_root, path=path)