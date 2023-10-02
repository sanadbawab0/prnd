from django.urls import path
from . import views

urlpatterns = [
    path('maintenance-centers/', views.get_maintenance_centers, name='maintenance_centers'), 
    path('maintenance-center/<int:pk>/', views.get_maintenance_center, name='maintenance_centers'), 
    path('add-maintenance-center/', views.add_maintenance_center, name='add_maintenance_centers'), 
    path('edit-maintenance-center/<int:pk>/', views.edit_maintenance_center, name='edit_maintenance_center'), 
    path('delete-maintenance-center/<int:pk>/', views.delete_maintenance_center, name='delete_maintenance_center'), 
    ]

