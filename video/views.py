from django.views.static import serve
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from video.models import Movie, Serie
from video.serializers import MovieSerializer, SeriesSerializer
from videoflix_backend import settings

CACHETTL = 60


class MovieView(APIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [permissions.AllowAny]

    @method_decorator(cache_page(CACHETTL))
    def get(self, request):
        serializer = MovieSerializer(self.queryset.all(), many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

class SeriesView(APIView):
    queryset = Serie.objects.all()
    serializer_class = SeriesSerializer
    permission_classes = [permissions.AllowAny]

    @method_decorator(cache_page(CACHETTL))
    def get(self, request):
        serializer = SeriesSerializer(self.queryset.all(), many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

class MovieSeriesView(APIView):
    permission_classes = [permissions.AllowAny]

    @method_decorator(cache_page(CACHETTL))
    def get(self, request):
        movie_serializer = MovieSerializer(Movie.objects.all(), many=True)
        series_serializer = SeriesSerializer(Serie.objects.all(), many=True)
        data = {'movies': movie_serializer.data, 'series':series_serializer.data}
        return Response(data=data, status=status.HTTP_200_OK)

class MediaView(APIView):
    permission_classes = [permissions.AllowAny]

    @method_decorator(cache_page(CACHETTL))
    def get(self, request, path):
        document_root = settings.MEDIA_ROOT
        return serve(request, document_root=document_root, path=path)
