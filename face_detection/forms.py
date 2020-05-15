from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import ImageModel

# forma koja nasleđuje UserCreationForm koja je default forma za kreiranje korisnika u Djangu
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User #forma je kreirana po modelu User
        fields = ['username', 'email', 'password1', 'password2'] #polja koja će biti prikazana na formi

# forma koja će se koristiti za upload slika
class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = ImageModel #forma je kreirana po modelu ImageModel
        fields = ('description', 'document') #polja koja će biti prikazana na formi

