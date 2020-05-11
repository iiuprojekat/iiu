from django.contrib import admin
from .models import ImageModel,DetectionModel
# Register your models here.

admin.site.register(ImageModel)
admin.site.register(DetectionModel)
