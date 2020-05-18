from django.conf import settings
import numpy as np
import cv2


def opencv_dface(path):
    # broj detektovanih lica postavljamo na 0
    detected_faces = 0
    # cv2.imread uzima 2 parametera, prvi je putanja slike a drugi je format u kom želiš da učitaš sliku
    # ukoliko je veći od 0 - čita BGR format - uključuje plavi, zeleni i crveni kanal
    img = cv2.imread(path, 1)

    # ispituje uslov da li je tip slike numpy array (niz)
    if type(img) is np.ndarray:
        # štampa uređenu n-torku (tuple) od brojeva - redovi, kolone i broj kanala
        print(img.shape)

        # učitavanje baseUrl-a gde se nalaze xml klasifikatori
        # učitavanje potrebnog xml klasifikatora
        baseUrl = settings.MEDIA_ROOT_URL + settings.MEDIA_URL
        face_cascade = cv2.CascadeClassifier(baseUrl + 'cascades/haarcascade_frontalface_default.xml')
        # učitava sliku u grayscale mode-u
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # nalazimo lica na slici, ako se pronađu lica, vraća pozicije otkrivenih lica kao pravougaonik(x, y, w, h)
        # jednom kada dobijemo ove lokacije(koordinate), možemo da stvorimo ROI (bounding box) za lice
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        # vraća broj lica
        detected_faces = len(faces)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = img[y:y + h, x:x + w]

        # upisivanje slike na zadatu putanju
        cv2.imwrite(path, img)

    else:
        # prikaz greške
        print('ERROR')
        print(path)
    # vraća broj detektovanih lica
    return detected_faces