from django.db import models
from django.contrib.auth.models import User
import django.contrib.auth


# model koji će se koristiti za upload slika
class ImageModel(models.Model):
    description = models.CharField(max_length=255, blank=True)  # opis modela
    document = models.ImageField(upload_to='images/%Y/%m/%d')  # polje za sliku koje definiše putanju na kojoj ce se čuvati slika u projektu
    uploaded_at = models.DateTimeField(auto_now_add=True)  # datum i vreme upload-a
    user = models.ForeignKey(django.contrib.auth.get_user_model(), null=True,
                             on_delete=models.CASCADE)  # foregin key koji povezuje sliku sa korisnikom koji ju je postavio


FILE_TYPES = (('IMAGE', 'IMAGE'), ('VIDEO', 'VIDEO'))


# model koji će se koristiti za čuvanje podataka o detekcijama
class DetectionModel(models.Model):
    file_name = models.CharField(max_length=255, blank=True)  # naziv fajla
    file_type = models.CharField(choices=FILE_TYPES, max_length=5)  # tip fajla koji moze biti IMAGE ili VIDEO
    detected_faces = models.PositiveSmallIntegerField()  # broj detektovanih lica
    date = models.CharField(max_length=255)  # polje za datum detekcije
    time = models.CharField(max_length=255)  # polje za vreme detekcije
    size = models.CharField(max_length=255)  # polje za velicinu fajla
    user = models.ForeignKey(django.contrib.auth.get_user_model(), null=True,
                             on_delete=models.CASCADE)  # foregin key koji povezuje detekciju sa korisnikom koji je napravio sliku/video
