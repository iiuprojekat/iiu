from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path
from django.views.generic import RedirectView

from face_detection.views import loginuser, logoutuser, register, homepage, detect
urlpatterns = [
    path('login/', loginuser, name="login"),
    path('logout/', logoutuser, name="logout"),
    path('register/', register, name="register"),
    path('', RedirectView.as_view(url="login/")),
    path('homepage/', homepage, name="homepage"),
    url(r'^detect/$', detect, name="detect"),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)