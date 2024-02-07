from rest_framework import serializers

from account.models import VideoflixUser


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = VideoflixUser
        fields = ['username', 'email', 'password']
        extra_kwargs = {'email': {'required': True}}