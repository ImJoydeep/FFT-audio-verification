from django.db import models

# Create your models here.
class AudioFile(models.Model):
    email = models.EmailField(max_length=100,default="fake@gmail.com")
    fft_data = models.TextField()
    audio = models.FileField(upload_to='login_audio/')

class User(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=100,default="fake@gmail.com")
    fft_features = models.TextField()
    audio_file = models.FileField(upload_to='register_audio/')
    

    def __str__(self):
        return self.audio_file