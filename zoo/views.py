from urllib import request
from webbrowser import get
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from zoo.admin import AnimalResource
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from zoo.decorators import allowed_users, unauthenticated_user, admin_only 

from .models import Animal, Enclosure, Animal_keeper, FeedingSchedule, Supplier, Supply, HealthCheck, Veterinarian
from django.http import HttpResponse
from django.views import View
from . import filters
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .form import AnimalForm, AnimalKeeperForm, AnimalUpdateForm, CreateUserForm, EnclosureForm, FeedingScheduleForm, HealthCheckForm, SupplierForm, SupplyForm, VeterinarianForm


@unauthenticated_user
def register_view(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='records-assistant')  # Assuming you have a group named 'user'
            user.groups.add(group)  # Add user to the group
            messages.success(request, 'Account was created for ' + username)
            return redirect('login')  # or wherever you want to redirect
    else:
        form = CreateUserForm()
    context ={
        'form': form,
    }
    return render(request, "register.html", context)

@unauthenticated_user
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)  # Make sure to log in the user first
            
            if user.groups.filter(name='admin').exists():
                return redirect('admin:index')
            else:
                return redirect('animal_list')
        else:
            messages.error(request, 'Enter a valid username and password!')
    
    return render(request, 'login.html')
    


def logout_view(request):
    logout(request)
    return redirect('login')


# @login_required(login_url= 'login')
from django.conf import settings

def home_view(request):
    if not request.user.is_authenticated:
        return redirect(f"{settings.LOGIN_URL}?next={request.path}")
    context = {}
    return render(request, 'home.html', context)



def userPage(request):
    context ={

    }
    return render(request, 'user.html', context)



# Create your views here.
class AnimalListView(LoginRequiredMixin, View):
    login_url = 'login'  # redirect URL for unauthenticated users
    
    def get(self, request):
        animals = Animal.objects.all()
        p = Paginator(Animal.objects.all(), 5)
        page = request.GET.get('page')
        animals_pg = p.get_page(page)
        animal_count= animals.count()
        myFilter=filters.AnimalFilter(request.GET, queryset=animals)
        animals = myFilter.qs  # Get the filtered queryset
        context ={

            'animals': animals,
            'myFilter': myFilter,
            'animal_count': animal_count,
            'animals_pg' :animals_pg
        }
        return render(request, 'animal/animal_list.html', context)


class AnimalDetailView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, animal_id):
        animal = get_object_or_404(Animal, id=animal_id)
        return render(request, 'animal/animal_detail.html', {'animal': animal})


# Add Animal View
@login_required(login_url= 'login')
def add_animals(request):
   form = AnimalForm(request.POST or None)
   if form.is_valid():
        form.save()
        messages.success(request, 'Animal record added successfully!')
        return redirect('animal_list')
   
   context = {
        "form": form,
        "title": "Add animal",
    }
   return render(request, "animal/add_animals.html", context)


@login_required(login_url= 'login')
def update_animal(request, animal_id):
    animal = get_object_or_404(Animal, id=animal_id)
    form = AnimalForm(instance=animal)

    if request.method == 'POST':
        form = AnimalForm(request.POST, instance=animal)
        if form.is_valid():
            form.save()
            messages.success(request, "Animal record updated successfully!")
            return redirect('animal_list')

    context = {
        "form": form,
        "title": "Update Animal Record",
    }
    return render(request, "animal/add_animals.html", context)


@login_required(login_url= 'login')
def delete_animal(request, animal_id):
    animal = Animal.objects.get(id=animal_id)
    if request.method == 'POST':
        animal.delete()
        messages.success(request, 'Animal record deleted successfully!')

        return redirect('/animal_list')
    return render(request, 'delete.html', {'obj': animal})


@login_required(login_url= 'login')
def export_animals_csv(request):
    dataset = AnimalResource().export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="animals.csv"'
    return response


@login_required(login_url= 'login')
def export_animals_xlsx(request):
    dataset = AnimalResource().export()
    response = HttpResponse(dataset.xlsx, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="animals.xlsx"'
    return response

class EnclosureListView(View):
    def get(self, request):
        enclosures = Enclosure.objects.all()
        enclosure_pg = Paginator(Enclosure.objects.all(), 5)
        page = request.GET.get('page')
        enclosures_pg = enclosure_pg.get_page(page)
        enclosures_count = enclosures.count()
        myFilter = filters.EnclosureFilter(request.GET, queryset=enclosures)
        enclosures = myFilter.qs  # Get the filtered queryset
        context = {
            'enclosures': enclosures,
            'myFilter': myFilter,
            'enclosures_count': enclosures_count,
            'enclosures_pg': enclosures_pg
        }
        return render(request, 'enclosure/enclosure_list.html', context)
    

   
@login_required(login_url= 'login')   
def add_enclosure(request):
    form = EnclosureForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Animal enclosure added successfully!')
        return redirect('enclosure_list')
    context = {
        "form": form,
        "title": "Add enclosure",
    }
    return render(request, "enclosure/add_enclosure.html", context)

@login_required(login_url= 'login')
def update_enclosure(request, enclosure_id):
    enclosure = Enclosure.objects.get(id=enclosure_id)
    form = EnclosureForm(instance=enclosure)
    if request.method == 'POST':
        form = EnclosureForm(request.POST, instance=enclosure)
    if form.is_valid():
        form.save()
        messages.success(request, 'Animal enclosure updated successfully!')
        return redirect('enclosure_list')
    context = {
        "form": form,
        "title": "Update enclosure",
    }
    return render(request, "enclosure/add_enclosure.html", context)


@login_required(login_url= 'login')
def delete_enclosure(request, enclosure_id):
    enclosure = Enclosure.objects.get(id=enclosure_id)
    if request.method == 'POST':
        enclosure.delete()
        messages.success(request, 'Animal enclosure deleted successfullt!')
        return redirect('enclosure_list')
    return render(request, 'delete.html', {'obj': enclosure})

class AnimalKeeperView(LoginRequiredMixin, View):
    login_url = 'login'  # redirect URL for unauthenticated users
    def get(self, request):
        animal_keeper = Animal_keeper.objects.all()
        p = Paginator(Animal_keeper.objects.all(), 5)
        page = request.GET.get('page')
        animal_keeper_pg = p.get_page(page)
        animal_keeper_count = animal_keeper.count()
        myFilter = filters.AnimalKeeperFilter(request.GET, queryset=animal_keeper)
        animal_keeper = myFilter.qs  # Get the filtered queryset    
        context = {
            'animal_keeper': animal_keeper,
            'myFilter': myFilter,
            'animal_keeper_count': animal_keeper_count,
            'animal_keeper_pg': animal_keeper_pg,
        }
        return render(request, 'keepers/keeper_list.html', context)


@login_required(login_url= 'login')
def add_animal_keeper(request):
    form = AnimalKeeperForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Animal keeper record added successfully!')
        return redirect('animal_keeper_list')
    context = {
        "form": form,
        "title": "Add animal keeper",
    }
    return render(request, "keepers/add_keeper.html", context)


@login_required(login_url= 'login')
def update_animal_keeper(request, animal_keeper_id):
    animal_keeper = Animal_keeper.objects.get(id=animal_keeper_id)
    form = AnimalKeeperForm(instance=animal_keeper)
    if request.method == 'POST':
        form = AnimalKeeperForm(request.POST, instance=animal_keeper)
    if form.is_valid():
        form.save()
        messages.success(request, 'Animal keeper record updated successfully!')
        return redirect('animal_keeper_list')
    
    context = {
        "form": form,
        "title": "Update animal keeper",
    }
    return render(request, "keepers/add_keeper.html", context)


@login_required(login_url= 'login')
def delete_animal_keeper(request, animal_keeper_id):
    animal_keeper = Animal_keeper.objects.get(id=animal_keeper_id)
    if request.method == 'POST':
        animal_keeper.delete()
        messages.success(request, 'Animal keeper record deleted successfully!')
        return redirect('animal_keeper_list')
    return render(request, 'delete.html', {'obj': animal_keeper})


@login_required(login_url= 'login')
def export_animal_keepers_csv(request):
    dataset = AnimalResource().export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="animal_keepers.csv"'
    return response


@login_required(login_url= 'login')
def export_animal_keepers_xlsx(request):
    dataset = AnimalResource().export()
    response = HttpResponse(dataset.xlsx, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="animal_keepers.xlsx"'
    return response


class FeedingScheduleView(LoginRequiredMixin, View):
    login_url = 'login'  # redirect URL for unauthenticated users
    def get(self, request):
        feeding_schedule = FeedingSchedule.objects.all()
        p = Paginator(FeedingSchedule.objects.all(), 5)
        page = request.GET.get('page')
        feeding_schedule_pg = p.get_page(page)
        # Count the total number of feeding schedules
        feeding_schedule_count = feeding_schedule.count()
        myFilter = filters.FeedingScheduleFilter(request.GET, queryset=feeding_schedule)
        feeding_schedule = myFilter.qs  # Get the filtered queryset
        context = {
            'feeding_schedule': feeding_schedule,
            'myFilter': myFilter,
            'feeding_schedule_count': feeding_schedule_count,
            'feeding_schedule_pg': feeding_schedule_pg,
        }
        return render(request, 'feeding/feeding_list.html', context)


@login_required(login_url='login')
def delete_animal_keeper(request, animal_keeper_id):
    animal_keeper = Animal_keeper.objects.get(id=animal_keeper_id)
    if request.method == 'POST':
        animal_keeper.delete()
        messages.success(request, 'Animal keeper record deleted successfully!')
        return redirect('animal_keeper_list')
    return render(request, 'delete.html', {'obj': animal_keeper})

@login_required(login_url='login')
def add_feeding_schedule(request):
    form = FeedingScheduleForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Feeding schedule added successfully!')
        return redirect('feeding_list')
    context = {
        "form": form,
        "title": "Add feeding schedule",
    }
    return render(request, "feeding/add_feeding.html", context)


@login_required(login_url= 'login')
def update_feeding_schedule(request, feeding_schedule_id):
    feeding_schedule = FeedingSchedule.objects.get(id=feeding_schedule_id)
    form = FeedingScheduleForm(instance=feeding_schedule)
    if request.method == 'POST':
        form = FeedingScheduleForm(request.POST, instance=feeding_schedule)
    if form.is_valid():
        form.save()
        messages.success(request, 'Feeding schedule updated successfully!')
        return redirect('feeding_list')
    context = {
        "form": form,
        "title": "Update feeding schedule",
    }
    return render(request, "feeding/add_feeding.html", context)


@login_required(login_url= 'login')
def delete_feeding_schedule(request, feeding_schedule_id):
    feeding_schedule = FeedingSchedule.objects.get(id=feeding_schedule_id)
    if request.method == 'POST':
        feeding_schedule.delete()
        messages.success(request, 'Feeding schedule deleted successfully!')
        return redirect('feeding_list')
    return render(request, 'delete.html', {'obj': feeding_schedule})


@login_required(login_url= 'login')
def export_feeding_schedule_csv(request):
    dataset = AnimalResource().export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="feeding_schedule.csv"'
    return response

@login_required(login_url= 'login')
def export_feeding_schedule_xlsx(request):      
    dataset = AnimalResource().export()
    response = HttpResponse(dataset.xlsx, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="feeding_schedule.xlsx"'
    return response


class SupplierView(LoginRequiredMixin, View):
    login_url = 'login'  # redirect URL for unauthenticated users
    def get(self, request):
        suppliers = Supplier.objects.all()
        p = Paginator(Supplier.objects.all(), 5)
        page = request.GET.get('page')
        suppliers_pg = p.get_page(page)
        # Count the total number of suppliers
        suppliers_count = suppliers.count()
        myFilter = filters.SupplierFilter(request.GET, queryset=suppliers)
        suppliers = myFilter.qs  # Get the filtered queryset
        context = {
            'suppliers': suppliers,
            'myFilter': myFilter,
            'suppliers_count': suppliers_count,
            'suppliers_pg': suppliers_pg,
        }
        return render(request, 'supplier/supplier_list.html', context)


@login_required(login_url='login')
def add_supplier(request):
    form = SupplierForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Supplier added successfully!')   
        return redirect('supplier_list')
    context = {
        "form": form,
        "title": "Add supplier",
    }
    return render(request, "supplier/add_supplier.html", context)  


@login_required(login_url= 'login')
def update_supplier(request, supplier_id):  
    supplier = Supplier.objects.get(id=supplier_id)
    form = SupplierForm(instance=supplier)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
    if form.is_valid():
        form.save()
        messages.success(request, 'Supplier updated successfully!')
        return redirect('supplier_list')
    context = {
        "form": form,
        "title": "Update supplier",
    }
    return render(request, "supplier/add_supplier.html", context)


@login_required(login_url= 'login')
def delete_supplier(request, supplier_id):
    supplier = Supplier.objects.get(id=supplier_id)
    if request.method == 'POST':
        supplier.delete()
        messages.success(request, 'Supplier deleted successfully!')
        return redirect('supplier_list')
    return render(request, 'delete.html', {'obj': supplier})


@login_required(login_url= 'login')
def export_suppliers_csv(request):  
    dataset = AnimalResource().export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="suppliers.csv"'
    return response

@login_required(login_url= 'login')
def export_suppliers_xlsx(request):
    dataset = AnimalResource().export()
    response = HttpResponse(dataset.xlsx, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="suppliers.xlsx"'
    return response

class SupplyView(LoginRequiredMixin, View):
    login_url = 'login'  # redirect URL for unauthenticated users
    def get(self, request):
        supplies = Supply.objects.all()
        p = Paginator(Supply.objects.all(), 5)
        page=request.GET.get('page')
        supplies_pg = p.get_page(page)
        supplies_count = supplies.count()
        myFilter = filters.SupplyFilter(request.GET, queryset=supplies)
        supplies = myFilter.qs
        context = {
            'supplies': supplies,
            'myFilter': myFilter,
            'supplies_count': supplies_count,
            'supplies_pg':supplies_pg
        }
        return render(request, 'supply/supply_list.html', context)
    
@login_required(login_url='login')
def add_supply(request):
    form = SupplyForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Supply added successfully!') 
        return redirect('supply_list')
    context = {
        "form": form,
        "title": "Add supply",
    }
    return render(request, "supply/add_supply.html", context)


@login_required(login_url= 'login')
def update_supply(request, supply_id):  
    supply = Supply.objects.get(id=supply_id)
    form = SupplyForm(instance=supply)
    if request.method == 'POST':
        form = SupplyForm(request.POST, instance=supply)
    if form.is_valid():
        form.save()
        messages.success(request, 'Supply updated successfully!')   
        return redirect('supply_list')
    context = {
        "form": form,
        "title": "Update supply",
    }
    return render(request, "supply/add_supply.html", context)


@login_required(login_url= 'login')
def delete_supply(request, supply_id):
    supply = Supply.objects.get(id=supply_id)
    if request.method == 'POST':
        supply.delete()
        messages.success(request, 'Supply deleted successfully!')   
        return redirect('supply_list')
    return render(request, 'delete.html', {'obj': supply})

@login_required(login_url= 'login')
def export_supplies_csv(request):
    dataset = AnimalResource().export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="supplies.csv"'
    return response

@login_required(login_url= 'login')
def export_supplies_xlsx(request):
    dataset = AnimalResource().export()
    response = HttpResponse(dataset.xlsx, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="supplies.xlsx"'
    return response

class HealthCheckView(LoginRequiredMixin, View):
    login_url = 'login'  # redirect URL for unauthenticated users
    def get(self, request):
        health_checks = HealthCheck.objects.all()
        p = Paginator(HealthCheck.objects.all(), 5)
        page = request.GET.get('page')
        health_checks_pg = p.get_page(page)
        health_checks_count = health_checks.count()
        myFilter = filters.HealthCheckFilter(request.GET, queryset=health_checks)
        health_checks = myFilter.qs
        context = {
            'health_checks': health_checks,
            'myFilter': myFilter,
            'health_checks_count': health_checks_count,
            'health_checks_pg': health_checks_pg
        }
        return render(request, 'health/health_list.html', context)

@login_required(login_url='login')
def add_health_check(request):
    form = HealthCheckForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Health check added successfully!')
        return redirect('health_check_list')
    context = {
        "form": form,
        "title": "Add health check",
    }
    return render(request, "health/add_health.html", context)


@login_required(login_url= 'login')
def update_health_check(request, health_check_id):  
    health_check = HealthCheck.objects.get(id=health_check_id)
    form = HealthCheckForm(instance=health_check)
    if request.method == 'POST':
        form = HealthCheckForm(request.POST, instance=health_check)
    if form.is_valid():
        form.save()
        messages.success(request, 'Health record updated successfully!')
        return redirect('health_check_list')
    context = {
        "form": form,
        "title": "Update health check",
    }
    return render(request, "health/add_health.html", context)


@login_required(login_url= 'login')
def delete_health_check(request, health_check_id):
    health_check = HealthCheck.objects.get(id=health_check_id)
    if request.method == 'POST':
        health_check.delete()
        messages.success(request, 'Health check deleted successfully!')
        return redirect('health_check_list')
    return render(request, 'delete.html', {'obj': health_check})

@login_required(login_url= 'login')
def export_health_checks_csv(request):
    dataset = AnimalResource().export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="health_checks.csv"'
    return response

@login_required(login_url= 'login')
def export_health_checks_xlsx(request):
    dataset = AnimalResource().export()
    response = HttpResponse(dataset.xlsx, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="health_checks.xlsx"'
    return response

class VeterinarianView(LoginRequiredMixin, View):
    def get(self, request):
        veterinarians = Veterinarian.objects.all()
        p = Paginator(Veterinarian.objects.all(), 5)
        page = request.GET.get('page')
        veterinarians_pg=p.get_page(page)
        veterinarians_count = veterinarians.count()
        myFilter = filters.VeterinarianFilter(request.GET, queryset=veterinarians)
        veterinarians = myFilter.qs  # Get the filtered queryset
        context = {
            'veterinarians': veterinarians,
            'myFilter': myFilter,
            'veterinarians_count': veterinarians_count,
            'veterinarians_pg': veterinarians_pg,
        }
        return render(request, 'vet/vet_list.html', context)


@login_required(login_url='login')
def add_veterinarian(request):
    form = VeterinarianForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Veterinarian added successfully!')
        return redirect('vet_list')
    context = {
        "form": form,
        "title": "Add veterinarian",
    }
    return render(request, "vet/add_vet.html", context)


@login_required(login_url= 'login')
def update_veterinarian(request, veterinarian_id):
    veterinarian = Veterinarian.objects.get(id=veterinarian_id)
    form = VeterinarianForm(instance=veterinarian)
    if request.method == 'POST':
        form = VeterinarianForm(request.POST, instance=veterinarian)
    if form.is_valid():
        form.save()
        messages.success(request, 'Veterinarian updated successfully!') 
        return redirect('vet_list')
    context = {
        "form": form,
        "title": "Update veterinarian",
    }
    return render(request, "vet/add_vet.html", context)


@login_required(login_url= 'login')
def delete_veterinarian(request, veterinarian_id):
    veterinarian = Veterinarian.objects.get(id=veterinarian_id)
    if request.method == 'POST':
        veterinarian.delete()
        messages.success(request, 'Veterinarian deleted successfully!')
        return redirect('vet_list')
    return render(request, 'delete.html', {'obj': veterinarian})

@login_required(login_url= 'login')
def export_veterinariaenclosure_lists_csv(request):  
    dataset = AnimalResource().export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="veterinarians_lists.csv"'
    return response


@login_required(login_url='login')
def export_veterinarians_xlsx(request):
    dataset = AnimalResource().export()
    response = HttpResponse(dataset.xlsx, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="veterinarians.xlsx"'
    return response

@login_required(login_url='login')
def export_animals_pdf(request):
    dataset = AnimalResource().export()
    response = HttpResponse(dataset.pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="animals.pdf"'
    return response

@login_required(login_url= 'login')
def export_animal_keepers_pdf(request):
    dataset = AnimalResource().export()
    response = HttpResponse(dataset.pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="animal_keepers.pdf"'
    return response

@login_required(login_url= 'login')
def export_feeding_schedule_pdf(request):
    dataset = AnimalResource().export()
    response = HttpResponse(dataset.pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="feeding_schedule.pdf"'
    return response

@login_required(login_url= 'login')
def export_suppliers_pdf(request):
    dataset = AnimalResource().export()
    response = HttpResponse(dataset.pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="suppliers.pdf"'
    return response

@login_required(login_url= 'login')
def export_supplies_pdf(request):
    dataset = AnimalResource().export()
    response = HttpResponse(dataset.pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="supplies.pdf"'
    return response

@login_required(login_url= 'login')
def export_health_checks_pdf(request):
    dataset = AnimalResource().export()
    response = HttpResponse(dataset.pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="health_checks.pdf"'
    return response

@login_required(login_url= 'login')
def export_veterinarians_pdf(request):
    dataset = AnimalResource().export()
    response = HttpResponse(dataset.pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="veterinarians.pdf"'
    return response 

@login_required(login_url= 'login')
def export_enclosures_pdf(request):
    dataset = AnimalResource().export()
    response = HttpResponse(dataset.pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="enclosures.pdf"'
    return response

@login_required(login_url= 'login')
def export_enclosures_csv(request):
    dataset = AnimalResource().export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="enclosures.csv"'
    return response

@login_required(login_url= 'login')
def export_enclosures_xlsx(request):
    dataset = AnimalResource().export()
    response = HttpResponse(dataset.xlsx, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="enclosures.xlsx"'
    return response

@login_required(login_url= 'login')
def export_enclosures_pdf(request):
    dataset = AnimalResource().export()
    response = HttpResponse(dataset.pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="enclosures.pdf"'
    return response