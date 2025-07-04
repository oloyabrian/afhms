import django_filters

from .models import *

class AnimalFilter(django_filters.FilterSet):
    class Meta:
        model = Animal
        fields = {
            'gender': ['exact'],
            'health_status': ['exact'],
            'enclosure__name': ['icontains'],
        }