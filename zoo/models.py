from django.db import models
from decimal import ROUND_HALF_UP, Decimal
from datetime import timezone
import datetime



class Zoo(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Animal(models.Model):
    name = models.CharField(max_length=100)
    family = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    health_status = models.CharField(max_length=100, choices=[('Healthy', 'Healthy'), ('Sick', 'Sick')])
    enclosure = models.ForeignKey('Enclosure', on_delete=models.CASCADE)
    arrival_date = models.DateField(default=datetime.date.today())
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Enclosure(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)   
    capacity = models.IntegerField()
    curent_occupancy = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class Animal_keeper(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    telephone = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    hire_date = models.DateField(default=datetime.date.today())
    enclosure_id = models.ForeignKey(Enclosure, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"



class FeedingSchedule(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    feeding_time = models.TimeField()
    food_type = models.CharField(max_length=100)
    quantity = models.FloatField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.animal.name} - {self.feeding_time}"

class Veterinarian(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    telephone = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    hire_date = models.DateField(default=datetime.date.today())
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class HealthCheck(models.Model):   
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    checkup_date = models.DateField(default=datetime.date.today())
    weight = models.FloatField()
    health_status = models.CharField(max_length=100, choices=[('Healthy', 'Healthy'), ('Sick', 'Sick')])
    temperature = models.FloatField(null=True, blank=True)
    diagnosis = models.CharField(max_length=100, null=True, blank=True)
    treatment = models.CharField(max_length=100, null=True, blank=True)
    veterinarian = models.ForeignKey(Veterinarian, on_delete=models.CASCADE)
    medication = models.CharField(max_length=100, null=True, blank=True)
    follow_up_date = models.DateField(default=datetime.date.today())
    follow_up_notes = models.DateField(default=datetime.date.today())
    next_checkup = models.DateField(default=datetime.date.today())
    notes = models.TextField(null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.animal.name} - {self.checkup_date}"
    

class Supplier(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    company_type = models.CharField(max_length=100)
    company_registration_number = models.CharField(max_length=100)
    company_address = models.TextField(null=True, blank=True)
    company_phone = models.CharField(max_length=100)
    company_email = models.EmailField(null=True, blank=True)
    company_website = models.URLField(null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name + " " + self.last_name
    
class Supply(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    supply_type = models.CharField(max_length=100)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
   
    @property
    def total_price(self):
        total = self.unit_price * self.quantity
        return total.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    def __str__(self):
        return f"{self.supply_type} - {self.supplier.first_name} {self.supplier.last_name}"

    def total_price_display(self):
        return f"${self.total_price:.2f}"

    total_price_display.short_description = "Total Price"

    delivery_date = models.DateField(default=datetime.date.today())
    date_added = models.DateTimeField(auto_now_add=True)