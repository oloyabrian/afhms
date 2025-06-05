from typing import __all__
from django.forms import ModelForm
from django import forms
from .models import Animal, Enclosure, Animal_keeper, FeedingSchedule, Supplier, Supply, HealthCheck, Veterinarian
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class AnimalForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = '__all__'

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError('This field is required.')

        # Exclude the current instance when checking for duplicates
        qs = Animal.objects.filter(name__iexact=name)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError(f"An animal with the name '{name}' already exists.")
        return name


class AnimalKeeperForm(forms.ModelForm):
    class Meta:
        model = Animal_keeper
        fields = '__all__'
        # fields = ['first_name', 'last_name','position', 'telephone', 'email', 'hire_date','enclosure_id' ]
     

class EnclosureForm(forms.ModelForm):
    class Meta:
        model = Enclosure
        fields = ['name', 'type', 'location', 'curent_occupancy','description', 'capacity']

class FeedingScheduleForm(forms.ModelForm):
    class Meta:
        model = FeedingSchedule
        fields = '__all__'
        # fields = ['animal', 'feeding_time', 'food_type', 'quantity']

       
class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['first_name', 'last_name', 'company_name', 'company_type', 'company_registration_number', 'company_address', 'company_phone', 'company_email']
 

class SupplyForm(forms.ModelForm):
    class Meta:
        model = Supply
        fields = '__all__'
        # fields =  ['supplier', 'supply_type', 'quantity', 'unit_price', 'delivery_date']


class HealthCheckForm(forms.ModelForm):
    class Meta:
        model = HealthCheck
        fields = ['animal', 'checkup_date', 'weight', 'health_status','diagnosis','treatment', 'veterinarian','medication', 'notes']
     

class VeterinarianForm(forms.ModelForm):
    class Meta:
        model = Veterinarian
        fields = ['first_name', 'last_name', 'specialization', 'telephone', 'email', 'address', 'hire_date']


#Form update of data in the database
class AnimalUpdateForm(forms.ModelForm):
	class Meta:
		model = Animal
		fields = ['name', 'family', 'breed', 'age', 'gender', 'health_status', 'arrival_date', 'enclosure']

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


