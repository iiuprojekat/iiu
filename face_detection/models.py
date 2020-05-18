from django.db import models
from django.contrib.auth.models import User

# Create your models here.
import django.contrib.auth

from iot_project import settings


# model koji će se koristiti za upload slika
class ImageModel(models.Model):
    description = models.CharField(max_length=255, blank=True)  # opis modela
    document = models.ImageField(upload_to='images/%Y/%m/%d')  # putanja na kojoj ce se cuvati slika u projektu
    uploaded_at = models.DateTimeField(auto_now_add=True)  # datum i vreme upload-a
    user = models.ForeignKey(django.contrib.auth.get_user_model(), null=True,
                             on_delete=models.CASCADE)  # foregin key koji povezuje sliku sa korisnikom koji ju je postavio


FILE_TYPES = (('IMAGE', 'IMAGE'), ('VIDEO', 'VIDEO'))


class DetectionModel(models.Model):
    file_name = models.CharField(max_length=255, blank=True)
    file_type = models.CharField(choices=FILE_TYPES, max_length=5)
    detected_faces = models.PositiveSmallIntegerField()
    date = models.CharField(max_length=255)
    time = models.CharField(max_length=255)
    size = models.CharField(max_length=255)
    user = models.ForeignKey(django.contrib.auth.get_user_model(), null=True, on_delete=models.CASCADE)
