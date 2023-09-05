from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path('register/', Register, name='register'),
    path('login/', Login, name='login'),
    path('user/', UserView, name='user'),
    path('logout/', Logout, name='logout'),
    path('edit-profile/', EditProfile, name='edit_profile'),
    # Other URL patterns
]
