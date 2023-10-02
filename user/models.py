from django.db import models
# from django.contrib.auth.models import User
import uuid
from phonenumber_field.modelfields import PhoneNumberField
from PIL import Image
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=35, )
    last_name = models.CharField(max_length=35,)
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=35, unique=True)
    phone_number = PhoneNumberField(blank=True, null=True)
    password = models.CharField(max_length=35)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']


class Profile(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    profile_image = models.ImageField(
        null=True, blank=True, upload_to='profiles', default="profiles/user-default.png")
    created = models.DateTimeField(auto_now_add=True)
    favorite_cars = models.ManyToManyField(
        'car.Car', related_name='favorited_by')
    favorite_posts = models.ManyToManyField(
        'news_and_articles.NewsAndArticles', related_name='favorited_by')
    followers = models.ManyToManyField('self', symmetrical=False, blank=True)

    def __str__(self):
        return str(self.user.username)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.profile_image.path)

        if img.width > 300 or img.height > 300:
            img.thumbnail((300, 300))
            img.save(self.profile_image.path)
