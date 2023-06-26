from django.http import JsonResponse, HttpResponse
from .models import AudioFile
from .utils import calculate_fft, matching_algorithm
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User, AudioFile
from .serializers import UserSerializer,LoginSerializer
import audioread
import numpy as np
import librosa
import os
@api_view(['POST'])
def register_user(request):
    username = request.data.get('username')
    email = request.data.get('email')
    audio_file = request.FILES.get('audio')

    # encoded_audio = base64.b64decode(audio_file.read())

    user_obj = User()
    user_obj.username = username
    user_obj.email = email
    user_obj.audio_file = audio_file
    user_obj.save()

    audio = User.objects.last()
    audio_url = str(audio.audio_file.path)

    audio_data, sample_rate = librosa.load(audio_url)
    fft_result = calculate_fft(audio_data)

    user_obj.fft_features = fft_result
    user_obj.save()
    serializer = UserSerializer(user_obj)

    return Response(serializer.data)

@api_view(['POST'])
def login_user(request):
    email = request.data.get('email')
    audio_file = request.FILES.get('audio')

    user_obj = AudioFile()
    user_obj.email = email
    user_obj.audio = audio_file
    user_obj.save()

    audio = AudioFile.objects.last()
    audio_url = str(audio.audio.path)

    # Perform FFT and extract features from audio file
    audio_data, sample_rate = librosa.load(audio_url)
    fft_result = calculate_fft(audio_data)
    # Extract relevant features from the FFT result

    users = User.objects.all()
    best_match = None
    best_match_score = 0.0

    for user in users:
        # Compare the extracted features with stored features using a matching algorithm
        match_score = matching_algorithm(fft_result, user.fft_features)
        if match_score > best_match_score:
            best_match = user
            best_match_score = match_score

    user_obj.fft_data = fft_result
    user_obj.save()
    if best_match is not None:
        serializer = UserSerializer(best_match)
        return Response(serializer.data)
    else:
        return Response('Invalid credentials')




