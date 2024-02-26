from rest_framework import serializers
from rest_framework.response import Response

from video.models import Movie, Episode, Serie


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = '__all__'

class SeriesSerializer(serializers.ModelSerializer):
    episodes = EpisodeSerializer(many=True, read_only=True)
    class Meta:
        model = Serie
        fields = '__all__'