from django.urls import path
from . import views

urlpatterns = [
    
    path('cars/<str:pk>/', views.get_car_details, name='get_car_details'),
    path('cars', views.get_cars, name='get_cars'),
]
