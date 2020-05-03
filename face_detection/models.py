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
