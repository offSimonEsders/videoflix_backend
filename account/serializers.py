from rest_framework import serializers

from account.models import VideoflixUser


class RegistrationSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = VideoflixUser
        fields = ['username', 'email', 'password']
        extra_kwargs = {'email': {'required': True}}

class LoginSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = VideoflixUser
        fields = ['email', 'password']
        extra_kwargs = {'email': {'required': True}}

class TokenSerializer(serializers.HyperlinkedModelSerializer):
    token = serializers.CharField()

    class Meta:
        fields = ['token']