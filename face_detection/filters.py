import django_filters
from .models import DetectionModel, ImageModel
from django_filters import DateFilter, CharFilter


#filter koji će se koristiti za pretragu detekcija
class DetectionFilter(django_filters.FilterSet):
    name = CharFilter(field_name='file_name', lookup_expr='icontains') #polje za pretagu po delu naziva

    class Meta:
        model = DetectionModel #model po kome se pravi filter
        fields = "__all__"
        exclude = ['user', 'size', 'date', 'time', 'file_name'] #polja koja se isključuju iz pretrage


class ImageFilter(django_filters.FilterSet):
    description = CharFilter(field_name='description', lookup_expr='icontains') #polje za pretragu po delu opisa
    start_date = DateFilter(field_name='uploaded_at', lookup_expr='gte') #polje za pretragu slika koje su posatvljene posle nekog datuma
    end_date = DateFilter(field_name='uploaded_at', lookup_expr='lte') #polje za pretragu slika koje su postavljene pre nekog datuma

    class Meta:
        model = ImageModel #model po kome se pravi filter
        fields = "__all__"
        exclude = ['user', 'document', 'uploaded_at'] #polja koja se isključuju iz pretrage
