# zoo/resources.py
from import_export import resources
from .models import Animal

class AnimalResource(resources.ModelResource):
    class Meta:
        model = Animal
# zoo/resources.py
from import_export import resources
from .models import Animal, FeedingSchedule, Supplier, HealthCheck

class AnimalResource(resources.ModelResource):
    class Meta:
        model = Animal

class FeedingScheduleResource(resources.ModelResource):
    class Meta:
        model = FeedingSchedule

class SupplierResource(resources.ModelResource):
    class Meta:
        model = Supplier

class HealthCheckResource(resources.ModelResource):
    class Meta:
        model = HealthCheck
