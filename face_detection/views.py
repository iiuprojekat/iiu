import os

from cv2 import cv2
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.csrf import csrf_protect

from iot_project.settings import BASE_DIR, MEDIA_ROOT
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
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():

            post = form.save(commit=False)
            post.user = request.user
            post.save()
            imageURL = settings.MEDIA_URL + form.instance.document.name
            opencv_dface(settings.MEDIA_ROOT_URL + imageURL)

            return render(request, 'face_detection/detect.html', {'form': form, 'post': post})
    else:
        form = ImageUploadForm()
    return render(request, 'face_detection/detect.html', {'form': form})

def face(request):
    return render(request, 'face_detection/face.html')

img_counter = 1
def detection(request, img_counter=img_counter):
    faceDetect = cv2.CascadeClassifier(MEDIA_ROOT+'/cascades/haarcascade_frontalface_default.xml')

    cam = cv2.VideoCapture(0)


    while(True):
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceDetect.detectMultiScale(gray, 1.3, 5)
        for(x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h), (0,255,0), 2)

        cv2.imshow("Face",img)
        if(cv2.waitKey(1) == ord('q')):
            img_name = f"opencv_frame_{format(img_counter)}.png"
            cv2.imwrite(img_name, img)
            print(f"{format(img_name)} written!")
            img_counter += 1
            cam.release()
            cv2.destroyAllWindows()
            return redirect('/face')
        # elif(cv2.waitKey(1) == ord('esc')):
        #     break

    # cam.release()
    # cv2.destroyAllWindows()
    # return redirect('/')

file_counter = 1
def detectionVideo(request, file_counter=file_counter):
    filename = f'video{file_counter}.avi'
    frames_per_second = 24.0
    res = '720p'
    faceDetect = cv2.CascadeClassifier(MEDIA_ROOT+'/cascades/haarcascade_frontalface_default.xml')

    cam = cv2.VideoCapture(0)
    out = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'XVID'), 25, (640, 480))
    # out = cv2.VideoWriter(filename, get_video_type(filename), 25, get_dims(cam, res))

    while(True):
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceDetect.detectMultiScale(gray, 1.3, 5)
        for(x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h), (0,255,0), 2)

        out.write(img)
        cv2.imshow("Face",img)

        if(cv2.waitKey(1) == ord('q')):
            print(f"{format(filename)} written!")
            file_counter += 1
            break
    cam.release()
    out.release()
    cv2.destroyAllWindows()
    return redirect('/face')



