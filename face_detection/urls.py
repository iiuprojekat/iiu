from django.urls import path
from django.views.generic import RedirectView

from face_detection.views import loginuser, logoutuser, register, homepage
urlpatterns = [
    path('login/', loginuser, name="login"),
    path('logout/', logoutuser, name="logout"),
    path('register/', register, name="register"),
    path('', RedirectView.as_view(url="login/")),
    path('homepage/', homepage, name="homepage")
]
