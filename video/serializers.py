from rest_framework import serializers
from rest_framework.response import Response

from video.models import Video


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'