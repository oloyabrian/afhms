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


@login_required(login_url= 'login')
@allowed_users(allowed_roles=['admin'])
def homePage(request):
    return redirect('admin:index')



def userPage(request):
    context ={

    }
    return render(request, 'user.html', context)



# Create your views here.
class AnimalListView(LoginRequiredMixin, View):
    login_url = 'login'  # redirect URL for unauthenticated users

    def get(self, request):
        animals = Animal.objects.all()
        return render(request, 'animal/animal_list.html', {'animals': animals})


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
        return redirect('/animal_list')
    messages.success(request, 'Animal record deleted successfully!')
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
        return render(request, 'enclosure/enclosure_list.html', {'enclosures': enclosures})
    

   
@login_required(login_url= 'login')   
def add_enclosure(request):
    form = EnclosureForm(request.POST or None)
    if form.is_valid():
        form.save()
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
        return redirect('enclosure_list')
    return render(request, 'delete.html', {'obj': enclosure})

class AnimalKeeperView(View):
    def get(self, request):
        animal_keeper = Animal_keeper.objects.all()
        return render(request, 'keepers/keeper_list.html', {'animal_keeper': animal_keeper})


@login_required(login_url= 'login')
def add_animal_keeper(request):
    form = AnimalKeeperForm(request.POST or None)
    if form.is_valid():
        form.save()
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


class FeedingScheduleView(View):
    def get(self, request):
        feeding_schedule = FeedingSchedule.objects.all()
        return render(request, 'feeding/feeding_list.html', {'feeding_schedule': feeding_schedule})



@login_required(login_url= 'login')
def add_feeding_schedule(request):
    form = FeedingScheduleForm(request.POST or None)
    if form.is_valid():
        form.save()
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


class SupplierView(View):
    def get(self, request):
        suppliers = Supplier.objects.all()
        return render(request, 'supplier/supplier_list.html', {'suppliers': suppliers})


@login_required(login_url= 'login')
def add_supplier(request):
    form = SupplierForm(request.POST or None)
    if form.is_valid():
        form.save()
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

class SupplyView(View):
    def get(self, request):
        supplies = Supply.objects.all()
        return render(request, 'supply/supply_list.html', {'supplies': supplies})
    
@login_required(login_url= 'login')
def add_supply(request):
    form = SupplyForm(request.POST or None)
    if form.is_valid():
        form.save()
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

class HealthCheckView(View):
    def get(self, request):
        health_checks = HealthCheck.objects.all()
        return render(request, 'health/health_list.html', {'health_checks': health_checks})

@login_required(login_url= 'login')
def add_health_check(request):
    form = HealthCheckForm(request.POST or None)
    if form.is_valid():
        form.save()
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

class VeterinarianView(View):
    def get(self, request):
        veterinarians = Veterinarian.objects.all()
        return render(request, 'vet/vet_list.html', {'veterinarians': veterinarians})


@login_required(login_url= 'login')
def add_veterinarian(request):
    form = VeterinarianForm(request.POST or None)
    if form.is_valid():
        form.save()
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
        return redirect('vet_list')
    return render(request, 'delete.html', {'obj': veterinarian})

@login_required(login_url= 'login')
def export_veterinarians_csv(request):  
    dataset = AnimalResource().export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="veterinarians.csv"'
    return response


@login_required(login_url= 'login')
def export_veterinarians_xlsx(request):
    dataset = AnimalResource().export()
    response = HttpResponse(dataset.xlsx, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="veterinarians.xlsx"'
    return response

@login_required(login_url= 'login')
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