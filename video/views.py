from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.shortcuts import render
from django.views.static import serve
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from video.models import Video
from video.serializers import VideoSerializer
from videoflix_backend import settings

CACHETTL = 60 * 60 * 2


class VideoView(APIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAuthenticated]

    @method_decorator(cache_page(CACHETTL))
    def get(self, request):
        serializer = VideoSerializer(Video.objects.all(), many=True)
        return Response(data=serializer.data)

class MediaView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @method_decorator(cache_page(CACHETTL))
    def get(self, request, path):
        document_root = settings.MEDIA_ROOT
        return serve(request, document_root=document_root, path=path)
