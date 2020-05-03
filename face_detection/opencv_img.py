from django.conf import settings
import numpy as np
import cv2


def opencv_dface(path):
    img = cv2.imread(path, 1)

    if type(img) is np.ndarray:
        print(img.shape)

        baseUrl = settings.MEDIA_ROOT_URL + settings.MEDIA_URL
        face_cascade = cv2.CascadeClassifier(baseUrl + 'cascades/haarcascade_frontalface_default.xml')

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = img[y:y + h, x:x + w]

        cv2.imwrite(path, img)

    else:
        print('ERROR')
        print(path)
