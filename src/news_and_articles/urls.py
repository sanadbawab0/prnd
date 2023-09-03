from django.urls import path
from . import views

urlpatterns = [
    
    path('news-and-articles/', views.news_page, name='news_page'),
    path('news-and-articles/<str:pk>/', views.article, name='article'),
    path('edit-article/<str:pk>/', views.edit_article, name='edit_article'),
    path('delete-article/<str:pk>/', views.delete_article, name='delete_article'),

]
