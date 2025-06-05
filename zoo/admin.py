from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources

from .models import Animal, Enclosure, Animal_keeper, FeedingSchedule, Supplier, Supply, HealthCheck, Veterinarian
from .form import AnimalForm, AnimalKeeperForm, EnclosureForm, FeedingScheduleForm, SupplierForm, SupplyForm, HealthCheckForm, VeterinarianForm

# --- Resources for CSV Import/Export ---
class AnimalResource(resources.ModelResource):
    class Meta:
        model = Animal

class EnclosureResource(resources.ModelResource):
    class Meta:
        model = Enclosure

class AnimalKeeperResource(resources.ModelResource):
    class Meta:
        model = Animal_keeper

class FeedingScheduleResource(resources.ModelResource):
    class Meta:
        model = FeedingSchedule

class SupplierResource(resources.ModelResource):
    class Meta:
        model = Supplier

class SupplyResource(resources.ModelResource):
    class Meta:
        model = Supply

class HealthCheckResource(resources.ModelResource):
    class Meta:
        model = HealthCheck

class VeterinarianResource(resources.ModelResource):
    class Meta:
        model = Veterinarian


# --- Admin Classes with Import/Export + Forms ---
class AnimalCreateAdmin(ImportExportModelAdmin):
    resource_class = AnimalResource
    list_display = ['name', 'family', 'breed', 'age', 'gender', 'health_status', 'arrival_date', 'enclosure']
    form = AnimalForm
    list_filter = ["name", "family"]
    search_fields = ["name", "family"]

class Animal_KeeperCreatAdmin(ImportExportModelAdmin):
    resource_class = AnimalKeeperResource
    list_display = ['first_name', 'last_name', 'position', 'telephone', 'email', 'hire_date', 'enclosure_id', 'date_added']
    form = AnimalKeeperForm
    list_filter = ['first_name', 'last_name', 'position']
    search_fields = ['first_name', 'last_name', 'position']

class EncloureCreateAdmin(ImportExportModelAdmin):
    resource_class = EnclosureResource
    list_display = ['name', 'type', 'location', 'description', 'capacity', 'curent_occupancy']
    form = EnclosureForm
    list_filter = ['name', 'type']
    search_fields = ['name', 'type']

class FeedingScheduleCreateAdmin(ImportExportModelAdmin):
    resource_class = FeedingScheduleResource
    list_display = ['animal', 'feeding_time', 'food_type', 'quantity']
    form = FeedingScheduleForm
    list_filter = ['animal', 'feeding_time', 'food_type']
    search_fields = ['animal__name', 'feeding_time', 'food_type']

class SupplierCreateAdmin(ImportExportModelAdmin):
    resource_class = SupplierResource
    list_display = ['first_name', 'last_name', 'company_name', 'company_type', 'company_registration_number', 'company_address', 'company_phone', 'company_email', 'company_website']
    form = SupplierForm
    list_filter = ['first_name', 'last_name', 'company_name', 'company_type']
    search_fields = ['first_name', 'last_name', 'company_name', 'company_type']

class SupplyCreateAdmin(ImportExportModelAdmin):
    resource_class = SupplyResource
    list_display = ['supplier', 'supply_type', 'quantity', 'unit_price', 'delivery_date', 'total_price']
    form = SupplyForm
    list_filter = ['supplier', 'supply_type', 'delivery_date']
    search_fields = ['supplier__company_name', 'supply_type']

class HealthCheckAdmin(ImportExportModelAdmin):
    resource_class = HealthCheckResource
    list_display = ['animal', 'checkup_date', 'weight', 'health_status', 'diagnosis', 'treatment', 'veterinarian', 'medication', 'notes']
    form = VeterinarianForm
    list_filter = ['veterinarian__first_name', 'veterinarian__last_name', 'veterinarian__specialization']
    search_fields = ['first_name', 'last_name', 'specialization']

class VeterinarianAdmin(ImportExportModelAdmin):
    resource_class = VeterinarianResource
    list_display = ['first_name', 'last_name', 'specialization', 'telephone', 'email', 'address', 'hire_date']
    form = VeterinarianForm
    list_filter = ['first_name', 'last_name', 'specialization']
    search_fields = ['first_name', 'last_name', 'specialization']


# --- Registering Models with Admin ---
admin.site.register(Animal, AnimalCreateAdmin)
admin.site.register(Enclosure, EncloureCreateAdmin)
admin.site.register(Animal_keeper, Animal_KeeperCreatAdmin)
admin.site.register(FeedingSchedule, FeedingScheduleCreateAdmin)
admin.site.register(Supplier, SupplierCreateAdmin)
admin.site.register(Supply, SupplyCreateAdmin)
admin.site.register(HealthCheck, HealthCheckAdmin)
admin.site.register(Veterinarian, VeterinarianAdmin)
