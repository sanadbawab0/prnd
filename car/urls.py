from django.urls import path
from . import views

urlpatterns = [
    
    path('home/', views.home_page, name='home'),
    path('cars/', views.get_cars, name='cars'),
    path('cars/<str:pk>/', views.get_car_details, name='get_car_details'),
    path('ads/',views.all_ads_page, name = 'all_ads_page'),
    path('advanced-search/',views.advanced_search, name = 'advanced_search'),
    path('add-car/',views.add_car, name = 'add_car'),
    path('edit-car/<str:pk>/', views.edit_car, name='edit_car'),
    path('delete-car/<str:pk>/', views.delete_car, name='delete_car'),
    path('home/cars-by-budget',views.get_car_by_budget)
]
