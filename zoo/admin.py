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
    list_filter = ["gender", "family", 'health_status', 'enclosure']
    search_fields = ["name", "family"]
    list_editable = ['health_status', 'enclosure']
    list_per_page = 10

class Animal_KeeperCreatAdmin(ImportExportModelAdmin):
    resource_class = AnimalKeeperResource
    list_display = ['first_name', 'last_name', 'position', 'telephone', 'email', 'hire_date', 'enclosure_id', 'date_added']
    form = AnimalKeeperForm
    list_filter = ['position',]
    search_fields = ['first_name', 'last_name', 'position']
    list_per_page = 10

class EncloureCreateAdmin(ImportExportModelAdmin):
    resource_class = EnclosureResource
    list_display = ['name', 'type', 'location', 'description', 'capacity', 'curent_occupancy']
    form = EnclosureForm
    list_filter = ['capacity', 'type', 'location']
    search_fields = ['name', 'type']
    list_editable = ['curent_occupancy',]
    list_per_page = 10

class FeedingScheduleCreateAdmin(ImportExportModelAdmin):
    resource_class = FeedingScheduleResource
    list_display = ['animal', 'feeding_time', 'food_type', 'quantity']
    form = FeedingScheduleForm
    list_filter = ['animal', 'feeding_time', 'food_type']
    search_fields = ['animal__name', 'feeding_time', 'food_type']
    list_editable = ['food_type',]
    list_per_page = 10

class SupplierCreateAdmin(ImportExportModelAdmin):
    resource_class = SupplierResource
    list_display = ['first_name', 'last_name', 'company_name', 'company_type', 'company_registration_number', 'company_address', 'company_phone', 'company_email', 'company_website']
    form = SupplierForm
    list_filter = ['company_name', 'company_type']
    search_fields = ['first_name', 'last_name', 'company_name', 'company_type']
    list_per_page = 10

class SupplyCreateAdmin(ImportExportModelAdmin):
    resource_class = SupplyResource
    list_display = ['supplier', 'supply_type', 'quantity', 'unit_price', 'delivery_date', 'total_price']
    form = SupplyForm
    list_filter = ['supply_type', 'delivery_date']
    search_fields = ['supplier__company_name', 'supply_type']
    list_editable=['quantity', 'unit_price']
    list_per_page = 10


class HealthCheckAdmin(ImportExportModelAdmin):
    resource_class = HealthCheckResource
    list_display = ['animal', 'checkup_date', 'weight', 'health_status', 'diagnosis', 'treatment', 'veterinarian', 'medication', 'notes']
    form = VeterinarianForm
    list_filter = ['health_status', 'veterinarian', 'diagnosis', 'veterinarian__specialization']
    search_fields = ['animal__name', 'checkup_date', 'diagnosis']
    list_per_page = 10


class VeterinarianAdmin(ImportExportModelAdmin):
    resource_class = VeterinarianResource
    list_display = ['first_name', 'last_name', 'specialization', 'telephone', 'email', 'address', 'hire_date']
    form = VeterinarianForm
    list_filter = ['address', 'specialization']
    search_fields = ['first_name', 'last_name', 'specialization']
    list_per_page = 10


# --- Registering Models with Admin ---
admin.site.register(Animal, AnimalCreateAdmin)
admin.site.register(Enclosure, EncloureCreateAdmin)
admin.site.register(Animal_keeper, Animal_KeeperCreatAdmin)
admin.site.register(FeedingSchedule, FeedingScheduleCreateAdmin)
admin.site.register(Supplier, SupplierCreateAdmin)
admin.site.register(Supply, SupplyCreateAdmin)
admin.site.register(HealthCheck, HealthCheckAdmin)
admin.site.register(Veterinarian, VeterinarianAdmin)
