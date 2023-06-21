from django.views import View
from django.http import JsonResponse, HttpResponse
from .models import AudioFile
from .utils import calculate_fft, matching_algorithm
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer
import base64
import speech_recognition as spr
import numpy as np
import librosa

@api_view(['POST'])
def register_user(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    audio_file = request.FILES.get('audio')

    # encoded_audio = base64.b64decode(audio_file.read())


    user_obj = User()
    user_obj.username = username
    user_obj.audio_file = audio_file
    user_obj.save()

    audio = User.objects.last()
    audio_url = str(audio.audio_file.url)


    audio_data, sample_rate = librosa.load(audio_url)
    fft_result = np.fft.fft(audio_data)

    # Save the user information and audio file to the database
    user = User(username=username, email=email, password=password, audio_file=audio_file, fft_features=fft_result)
    user.save()
    serializer = UserSerializer(user)

    return Response(serializer.data)

@api_view(['POST'])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    audio_file = request.FILES.get('audio')

    # Perform FFT and extract features from audio file
    audio_data, sample_rate = librosa.load(audio_file)
    fft_result = np.fft.fft(audio_data)
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

    if best_match is not None and best_match.password == password:
        serializer = UserSerializer(best_match)
        return Response(serializer.data)
    else:
        return Response({'error': 'Invalid credentials'}, status=401)









