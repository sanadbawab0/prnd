from django.urls import path
from . import views

urlpatterns = [
    
    path('news-and-articles/', views.news_page, name='news_page'),

]
