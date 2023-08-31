from django.db import models
from django.contrib.auth.models import User
import uuid
from phonenumber_field.modelfields import PhoneNumberField
from PIL import Image
from django.core.exceptions import ValidationError
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null = True, blank = True)
    first_name = models.CharField(max_length=35, blank=True, null=True)
    last_name  = models.CharField(max_length=35,blank=True ,null=True )
    email = models.EmailField(max_length = 500, blank=True, null=True)
    username = models.CharField(max_length=35, blank =True, null =True)
    phone_number = PhoneNumberField(region='JO')
    location = models.CharField(max_length=100, blank =True, null =True)
    profile_image = models.ImageField(null =True, blank=True, upload_to='profiles', default ="profiles/user-default.png")
    created = models.DateTimeField(auto_now_add = True)
    num_posts = models.PositiveIntegerField(default=0, editable=False)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    favorite_cars = models.ManyToManyField('car.Car', related_name='favorited_by')

    def __str__(self):
       return str(self.username)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.profile_image.path)

        if img.width > 300 or img.height > 300:
            img.thumbnail((300,300))
            img.save(self.profile_image.path)
            
    def calculate_num_posts(self):
        self.num_posts = self.posts.count()
        self.save()

    def get_followers_count(self):
        return UserConnection.objects.filter(following=self.user).count()

    def get_following_count(self):
        return UserConnection.objects.filter(follower=self.user).count()
    
class UserConnection(models.Model):
    follower = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='followers')
    following = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='following')
    created = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.follower == self.following:
            raise ValidationError("A user cannot follow themselves.")
    
    def __str__(self):
       return f'{self.follower} followed {self.following}'