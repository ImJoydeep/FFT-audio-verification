from django.db import models

# Create your models here.
class AudioFile(models.Model):
    audio = models.FileField(upload_to='audio_files/')
    fft_data = models.JSONField()

class User(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    fft_features = models.TextField()
    audio_file = models.FileField(upload_to='audio_file/')
    

    def __str__(self):
        return self.audio_file