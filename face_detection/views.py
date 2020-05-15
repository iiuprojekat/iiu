import os
from cv2 import cv2
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.csrf import csrf_protect
from .models import DetectionModel, ImageModel
from iot_project.settings import BASE_DIR, MEDIA_ROOT
from .forms import CreateUserForm, ImageUploadForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .opencv_img import opencv_dface

#dekorator koji se koristi ukoliko postoji POST metoda
@csrf_protect
def loginuser(request): #funkcija za logovanje korisnika
    # ukoliko je korisnik već ulogovan vratiće da na početnu stranu
    if request.user.is_authenticated:
        return redirect('homepage')
    if request.method == "POST":
        username = request.POST.get("username") #uzima se uneto korisničko ime sa forme
        password = request.POST.get("password") #uzima se uneta šifra sa forme
        user = authenticate(request, username=username, password=password) #vrši se autentifikacija korisnika
        if user is not None: #ukoliko je autentifikacija uspešna korisnik se loguje i prelazi na početnu stranu
            login(request, user)
            return redirect('homepage')
        else:
            messages.info(request, "Username of password is incorrect.") #ako autentifikacija nije uspešna vraća se poruka
    return render(request, 'face_detection/login.html')#renderuje se početna strana

#funkcija koja omogućava korisniku da se izloguje
def logoutuser(request):
    logout(request) #ugrađena funkcija za logout
    return redirect('login') #korisnik se vraća na login stranu

#dekorator koji se koristi ukoliko postoji POST metoda
@csrf_protect
def register(request): #funkcija koja omogućava korisniku da se registruje
    # ukoliko je korisnik već ulogovan vratiće da na početnu stranu
    if request.user.is_authenticated:
        return redirect('homepage')
    else:
        form = CreateUserForm()  # koristimo formu za kreiranje korisnika koja je definisana u okviru forms.py
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():  # funkcija proverava da li su podaci iz forme validni
                form.save()  # funkcija kreira novog korisnika
                user = form.cleaned_data.get("username") #funkacija uzima korisničko ime koje će koristiti u poruci
                messages.success(request, f"Account was created for {user} ") #ukoliko je kreiran novi korisnik, vraća se poruka
                return redirect('login') #prebacuje se na login stranicu
            else: #ukoliko forma nije validna
                pass1 = form.cleaned_data.get("password1") #uzima se prva unešena šifra
                pass2 = form.cleaned_data.get("password2") #uzim se druga unešena šifra
                if pass1 != pass2: #provera toga da li su dve unete šifre iste
                    messages.info(request, "The two password fields didn’t match.")
                else: #u suprotnom znači da je korisničko ime već zauzeto
                    messages.info(request, "Username is taken.")

        context = {'form': form}
        return render(request, 'face_detection/register.html', context) #renderovanje stranice za registrovanje

#dekorator koji omogućava da pristup početnoj strani bude dozoljen samo ulogovanim korisnicima
@login_required(login_url='login')
def homepage(request): #funkacija koja vraća početnu stranu
    detections = DetectionModel.objects.filter(user=request.user).order_by('-date', '-time') #kupljenje podataka koji će se prikazivati na strani
    return render(request, 'face_detection/homepage.html', {'detections': detections}) #renderovanje početne strane


@csrf_protect #dekorator koji se koristi ukoliko postoji POST metoda
@login_required(login_url='login') #dekorator koji omogućava da pristup početnoj strani bude dozoljen samo ulogovanim korisnicima
def detect(request): #detektovanje lica na upload-ovanim slikama
    uploads = ImageModel.objects.filter(user=request.user).order_by('-uploaded_at') #uzimanje podataka o prethodno uploadovanim slikama
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES) #kreiranje ImageUploadForm forme
        if form.is_valid(): #validacija forme
            post = form.save(commit=False) #čuvanje podataka sa forme
            post.user = request.user #postvaljanje id-a trenutno ulogovanog korisnika
            post.save() #čuvanje novog ImageModel-a u bazi
            imageURL = settings.MEDIA_URL + form.instance.document.name #putanja do sačuvane slike u projektu
            detected_faces = opencv_dface(settings.MEDIA_ROOT_URL + imageURL) #pozivanje funkacije koja se nalazi u skripti opencv_img.py
            file = f'media/{form.instance.document.name}' #uzimanje sačuvane slike na kojoj su detektovana lica
            d = DetectionModel(file_name=str(form.instance.document.name).split('/')[-1], file_type='IMAGE',
                               detected_faces=detected_faces, date=datetime.now().strftime("%d.%m.%Y"),
                               time=datetime.now().strftime("%H:%M:%S"),
                               size=f"{round(os.stat(file).st_size / 1024, 3)}KB",
                               user=request.user) #čuvanje uploadovane slike u DecetionModel modelu
            d.save()
            return render(request, 'face_detection/detect.html', {'form': form, 'post': post, 'uploads': uploads}) #renderovanje detect strane
    else:
        form = ImageUploadForm() #kreiranje ImageUploadForm forme koja će se prikazivati na detect strani
    return render(request, 'face_detection/detect.html', {'form': form, 'uploads': uploads}) #renderovanje detect strane


@login_required(login_url='login')
def face(request):
    return render(request, 'face_detection/face.html')


@login_required(login_url='login')
def detection(request):
    faceDetect = cv2.CascadeClassifier(MEDIA_ROOT + '/cascades/haarcascade_frontalface_default.xml')

    cam = cv2.VideoCapture(0)

    while (True):
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceDetect.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow("Face", img)
        if cv2.waitKey(1) == ord('q'):
            img_counter = len(DetectionModel.objects.filter(file_type='IMAGE')) + 1
            img_name = f"image{format(img_counter)}.png"
            os.chdir(r"./files/images")
            cv2.imwrite(img_name, img)
            print(f"{format(img_name)} written!")
            d = DetectionModel(file_name=img_name, file_type='IMAGE', detected_faces=len(faces),
                               size=f"{round(os.stat(img_name).st_size / 1024, 3)}KB", user=request.user,
                               date=datetime.now().strftime("%d.%m.%Y"), time=datetime.now().strftime("%H:%M:%S"))
            d.save()
            os.chdir(os.path.dirname(os.path.dirname(os.getcwd())))
            cam.release()
            cv2.destroyAllWindows()
            return redirect('/face')
        elif cv2.waitKey(1) == ord('w'):
            cam.release()
            cv2.destroyAllWindows()
            return redirect('/face')

        # elif(cv2.waitKey(1) == ord('esc')):
        #     break

    # cam.release()
    # cv2.destroyAllWindows()
    # return redirect('/')


@login_required(login_url='login')
def detectionVideo(request):
    file_counter = len(DetectionModel.objects.filter(file_type='VIDEO')) + 1
    filename = f'video{file_counter}.avi'
    os.chdir(r"./files/videos")
    frames_per_second = 24.0
    res = '720p'
    faceDetect = cv2.CascadeClassifier(MEDIA_ROOT + '/cascades/haarcascade_frontalface_default.xml')

    cam = cv2.VideoCapture(0)
    out = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'XVID'), 25, (640, 480))
    # out = cv2.VideoWriter(filename, get_video_type(filename), 25, get_dims(cam, res))
    faces_num = 0;
    while True:
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceDetect.detectMultiScale(gray, 1.3, 5)
        if len(faces) > faces_num:
            faces_num = len(faces)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        out.write(img)
        cv2.imshow("Face", img)

        if cv2.waitKey(1) == ord('q'):
            print(f"{format(filename)} written!")
            break

    d = DetectionModel(file_name=filename, file_type='VIDEO', detected_faces=faces_num,
                       size=f"{round(os.stat(filename).st_size / 1024, 3)}KB", user=request.user,
                       date=datetime.now().strftime("%d.%m.%Y"), time=datetime.now().strftime("%H:%M:%S"))
    d.save()
    os.chdir(os.path.dirname(os.path.dirname(os.getcwd())))
    cam.release()
    out.release()
    cv2.destroyAllWindows()
    return redirect('/face')
