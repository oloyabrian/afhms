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

class EnclosureFilter(django_filters.FilterSet):
    class Meta:
        model = Enclosure
        fields = {
            'type': ['exact'],
            'capacity': ['gte', 'lte'],
        }   

class AnimalKeeperFilter(django_filters.FilterSet):
    class Meta:
        model = Animal_keeper
        fields = {
            'first_name': ['icontains'],
            'sex': ['exact'],
            'position': ['icontains'],
        }

class FeedingScheduleFilter(django_filters.FilterSet):
    class Meta:
        model = FeedingSchedule
        fields = {
            'animal__name': ['icontains'],
            'feeding_time': ['exact'],
            'food_type': ['icontains'],
        }   

class VeterinarianFilter(django_filters.FilterSet):
    class Meta:
        model = Veterinarian
        fields = {
            'first_name': ['icontains'],
            'last_name': ['icontains'],
            'sex': ['exact'],
            'specialization': ['icontains'],
        }

class HealthCheckFilter(django_filters.FilterSet):
    class Meta:
        model = HealthCheck
        fields = {
            'animal__name': ['icontains'],
            'veterinarian__first_name': ['icontains'],
            'health_status': ['exact'],
        }

class SupplierFilter(django_filters.FilterSet):
    class Meta:
        model = Supplier
        fields = {
            'sex': ['exact'],
            'company_type': ['exact'],
            'company_name': ['icontains'],
        }

class SupplyFilter(django_filters.FilterSet):
    class Meta:
        model = Supply
        fields = {
            'supplier__first_name': ['icontains'],
            'quantity': ['gte', 'lte'],
            'date_added': ['exact', 'gte', 'lte'],
        }

class AnimalHealthFilter(django_filters.FilterSet):
    class Meta:
        model = HealthCheck
        fields = {
            'animal__name': ['icontains'],
            'checkup_date': ['exact', 'gte', 'lte'],
            'health_status': ['exact'],
            'veterinarian__first_name': ['icontains'],
        }

