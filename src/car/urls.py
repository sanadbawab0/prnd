from django.urls import path
from . import views

urlpatterns = [
    
    path('home/', views.home_page, name='home'),
    path('cars/', views.get_cars, name='cars'),
    path('cars/<str:pk>/', views.get_car_details, name='get_car_details'),
    path('ads/',views.all_ads_page, name = 'all_ads_page')
]
