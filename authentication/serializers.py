from rest_framework import serializers
from .models import User,AudioFile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'audio_file', 'fft_features')

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioFile
        fields = ('id', 'audio', 'fft_data')

