from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path('register/', Register, name='register'),
    path('login/', Login, name='login'),
    path('profile/', UserProfile, name='user'),
    path('logout/', Logout, name='logout'),
    path('edit-profile/', EditProfile, name='edit_profile'),
    path('profiles/', get_profiles, name='get_profiles'),
    path('other-profile/<str:profile_id>',
         ViewOtherProfile, name='view_other_profiles'),
    # Other URL patterns
]
