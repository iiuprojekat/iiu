from django.db import models
from django.contrib.auth.models import User


# Create your models here.
import django.contrib.auth

from iot_project import settings


class ImageModel(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.ImageField(upload_to='images/%Y/%m/%d')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(django.contrib.auth.get_user_model(), null=True, on_delete= models.CASCADE)

FILE_TYPES = (('IMAGE','IMAGE'),('VIDEO','VIDEO'))
class DetectionModel(models.Model):
    file_name = models.CharField(max_length=255, blank=True)
    file_type = models.CharField(choices=FILE_TYPES,max_length=5)
    detected_faces = models.PositiveSmallIntegerField()
    date = models.CharField(max_length=255)
    time = models.CharField(max_length=255)
    size = models.CharField(max_length=255)
    user = models.ForeignKey(django.contrib.auth.get_user_model(), null=True, on_delete= models.CASCADE)
