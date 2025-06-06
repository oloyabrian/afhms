from django.contrib import admin


from django.urls import path

from zoo import views


urlpatterns = [
   path('admin/', admin.site.urls, name='admin'),
   # path('', views.homePage, name='h'),
   path('', views.home_view, name="home"),
   path('login/', views.login_view, name='login'),
   path('logout/', views.logout_view, name='logout'),
   path('register/', views.register_view, name='register'),
   path('user/', views.userPage, name='userpage'),


   path('animal_list/', views.AnimalListView.as_view(), name='animal_list'),
   path('add_animals/', views.add_animals, name='add_animals'),
   path('animal_detail/<int:animal_id>/', views.AnimalDetailView.as_view(), name='animal_detail'),
   path('update_animal/<int:animal_id>/', views.update_animal, name='update_animal'),
   path('delete_animal/<int:animal_id>/', views.delete_animal, name='delete_animal'),


   path('enclosure_list/', views.EnclosureListView.as_view(), name='enclosure_list'),
   path('add_enclosure/', views.add_enclosure, name='add_enclosure'),
   path('update_enclosure/<int:enclosure_id>/', views.update_enclosure, name='update_enclosure'),
   path('delete_enclosure/<int:enclosure_id>/', views.delete_enclosure, name='delete_enclosure'),


   path('animal_keeper_list/', views.AnimalKeeperView.as_view(), name='animal_keeper_list'),
   path('add_animal_keeper/', views.add_animal_keeper, name='add_animal_keeper'),
   path('update_animal_keeper/<int:animal_keeper_id>/', views.update_animal_keeper, name='update_animal_keeper'),
   path('delete_animal_keeper/<int:animal_keeper_id>/', views.delete_animal_keeper, name='delete_animal_keeper'),


   path('feeding_list/', views.FeedingScheduleView.as_view(), name='feeding_list'),
   path('add_feeding_schedule/', views.add_feeding_schedule, name='add_feeding_schedule'),
   path('update_feeding_schedule/<int:feeding_schedule_id>/', views.update_feeding_schedule, name='update_feeding_schedule'),
   path('delete_feeding_schedule/<int:feeding_schedule_id>/', views.delete_feeding_schedule, name='delete_feeding_schedule'),


   path('supply_list/', views.SupplyView.as_view(), name='supply_list'),
   path('add_supply/', views.add_supply, name='add_supply'),
   path('update_supply/<int:supply_id>/', views.update_supply, name='update_supply'),
   path('delete_supply/<int:supply_id>/', views.delete_supply, name='delete_supply'),


   path('supplier_list/', views.SupplierView.as_view(), name='supplier_list'),
   path('add_supplier/', views.add_supplier, name='add_supplier'),
   path('update_supplier/<int:supplier_id>/', views.update_supplier, name='update_supplier'),
   path('delete_supplier/<int:supplier_id>/', views.delete_supplier, name='delete_supplier'),


   path('health_check_list/', views.HealthCheckView.as_view(), name='health_check_list'),
   path('add_health_check/', views.add_health_check, name='add_health_check'),
   path('update_health_check/<int:health_check_id>/', views.update_health_check, name='update_health_check'),
   path('delete_health_check/<int:health_check_id>/', views.delete_health_check, name='delete_health_check'),


   path('vet_list/', views.VeterinarianView.as_view(), name='vet_list'),
   path('add_vet/', views.add_veterinarian, name='add_vet'),
   path('update_vet/<int:veterinarian_id>/', views.update_veterinarian, name='update_vet'),
   path('delete_vet/<int:veterinarian_id>/', views.delete_veterinarian, name='delete_vet'),
]