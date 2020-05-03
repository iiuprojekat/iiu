from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.csrf import csrf_protect

from .forms import CreateUserForm, ImageUploadForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
from .opencv_img import opencv_dface


@csrf_protect
def loginuser(request):
    if request.user.is_authenticated:
        return redirect('homepage')
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('homepage')
        else:
            messages.info(request, "Username of password is incorrect.")
    return render(request, 'face_detection/login.html')


def logoutuser(request):
    logout(request)
    return redirect('login')


@csrf_protect
def register(request):
    if request.user.is_authenticated:
        return redirect('homepage')
    else:
        form = CreateUserForm()  # koristimo defaulth Django formu za kreiranje korisnika
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():  # funkcija proverava da li je validan korisnik
                form.save()  # funkcija kreira novog korisnika
                user = form.cleaned_data.get("username")
                messages.success(request, f"Account was created for {user} ")
                return redirect('login')
            else:
                pass1 = form.cleaned_data.get("password1")
                pass2 = form.cleaned_data.get("password2")
                if pass1 != pass2:
                    messages.info(request, "The two password fields didn’t match.")
                else:
                    messages.info(request, "Username is taken.")

        context = {'form': form}
        return render(request, 'face_detection/register.html', context)


@login_required(login_url='login')
def homepage(request):
    context = {}
    return render(request, 'face_detection/homepage.html', context)


@csrf_protect
@login_required(login_url='login')
def detect(request):
    if request.method == 'POST':
        form = ImageUploadForm( request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            imageURL = settings.MEDIA_URL + form.instance.document.name
            opencv_dface(settings.MEDIA_ROOT_URL + imageURL)

            return render(request, 'face_detection/detect.html', {'form': form, 'post': post})
    else:
        form = ImageUploadForm()
    return render(request, 'face_detection/detect.html', {'form': form})
