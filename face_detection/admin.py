from django.contrib import admin
from .models import ImageModel,DetectionModel
# Register your models here.

admin.site.register(ImageModel) #registracija ImageModel modela
admin.site.register(DetectionModel) #registracija DetectionModel modela
