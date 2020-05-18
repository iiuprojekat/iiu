import django_filters
from .models import DetectionModel, ImageModel
from django_filters import DateFilter, CharFilter


class DetectionFilter(django_filters.FilterSet):
    name = CharFilter(field_name='file_name', lookup_expr='icontains')

    class Meta:
        model = DetectionModel
        fields = "__all__"
        exclude = ['user', 'size', 'date', 'time', 'file_name']


class ImageFilter(django_filters.FilterSet):
    description = CharFilter(field_name='description', lookup_expr='icontains')
    start_date = DateFilter(field_name='uploaded_at', lookup_expr='gte')
    end_date = DateFilter(field_name='uploaded_at', lookup_expr='lte')

    class Meta:
        model = ImageModel
        fields = "__all__"
        exclude = ['user', 'document', 'uploaded_at']
