from django.db import models
from django_countries.fields import CountryField
import uuid
from user.models import Profile
from maintenance.models import MaintenanceCenter
import pandas as pd
from django.utils import timezone
from django.core.exceptions import ValidationError

# Create your models here.


data = pd.read_csv("Data.csv") 
unique_makes = data["Make"].unique()
unique_model = data["Model"].unique()
unique_model.sort()

current_year = timezone.now().year

def car_image_interior_path(instance, filename):
    return f'interior/{instance.id}/{filename}'
def car_image_exterior_path(instance, filename):
    return f'exterior/{instance.id}/{filename}'

class Car(models.Model):
    
    BRAND_CHOICES = [(make, make) for make in unique_makes]
    YEAR_CHOICES = [(year, year) for year in range(1900, current_year + 2)]
    TRANSMISSION_CHOICES = (
        ('manual', 'Manual'),
        ('automatic', 'Automatic'))
    
    FUEL_CHOICES = (
        ('petrol','بنزين'),
        ('diesel','ديزل'),
        ('electric','كهرباء'),
        ('hybrid','هايبرد'),
        ('mild-hybrid','مايلد هايبرد'),
        ('plugin-hybrid','هايبرد - plugin'),
    )
    CONDITION_CHOICES = (('excelent','ممتازة'),
                         ('good','جيد'),
                         ('small-accident','حادث بسيط'),
                         ('accident','تعرضت لحادث'),
                         ('other','أخرى'))
    
    CUSTOM_CHOICES = (('yes','مجمرك'),
                      ('no','غير مجمرك'))
    
    BODY_CHOICES = (('bus','Bus'),
                    ('convertible','Convertible'),
                    ('Coupe','coupe'),
                    ('hatchback','Hatchback'),
                    ('sedan','Sedan'),
                    ('suv','SUV'),
                    ('pick-up','PickUp'),
                    ('truck','Truck'))
    id =  models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    owner = models.ForeignKey(Profile, null=True, on_delete=models.CASCADE, related_name='owned_cars')
    brand = models.CharField(max_length=50, choices=BRAND_CHOICES)
    model = models.CharField('model', max_length=50)
    country = CountryField()
    release_year = models.PositiveIntegerField(choices=YEAR_CHOICES)
    engine_size = models.PositiveIntegerField(blank=True, null=True)
    fuel_type = models.CharField(max_length=20,choices=FUEL_CHOICES, blank=True, null=True)
    transmission_type = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES, blank=True, null=True)
    weight = models.PositiveIntegerField(blank=True, null=True, )
    horse_power = models.PositiveIntegerField(blank=True, null=True)
    speed = models.PositiveBigIntegerField(blank=True, null=True)
    fuel_mileage = models.PositiveIntegerField(blank=True, null=True)
    Odometer = models.PositiveIntegerField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, blank=True, null=True)
    custom = models.CharField(max_length=20, choices=CUSTOM_CHOICES, blank=True, null=True)
    body_type = models.CharField(max_length=20, choices = BODY_CHOICES, blank=True, null=True)
    color = models.CharField(max_length=10, blank=True, null=True)
    interior = models.TextField(blank=True ,null=True )
    interior_image = models.ImageField(upload_to=car_image_interior_path, blank=True, null=True) 
    exterior = models.TextField(blank=True ,null=True)
    exterior_image = models.ImageField(upload_to=car_image_exterior_path, blank=True, null=True)
    performance = models.CharField(max_length=50, blank=True, null=True)
    performance_description = models.TextField(blank=True ,null=True)
    tags = models.ManyToManyField('Tag', related_name='tags', default=None, blank=True)
    tech_and_safety_features = models.ManyToManyField('TechAndSafetyFeatures', related_name='cars', blank=True, default = None)
    maintenance_centers = models.ManyToManyField(MaintenanceCenter, default=None, blank = True, related_name='maintenance_centers')

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(release_year__gte=1900) & models.Q(release_year__lte=current_year + 2), #TODO تخيل صرنا 2025  THIS YEAR + 1
                name="valid_release_year"
            )
        ]
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        PriceHistory.objects.create(price=self.price)

    def __str__(self):
        return f"{self.owner} - {self.brand} {self.model}"
    




class TechAndSafetyFeatures(models.Model):
    feature = models.CharField(max_length=50)
    description = models.TextField(blank=True ,null=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return f'{self.feature}'

class PriceHistory(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='price_history', null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.car} - {self.price} at {self.date}"
    
class Tag(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True ,null=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name
    
class PositiveAspect(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='positive_aspects')
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class NegativeAspect(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='negative_aspects')
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length = 200, blank = True)
    author = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.SET_NULL, related_name='owner')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='post')
    description = models.TextField(blank = True)
    liked_by = models.ManyToManyField(Profile, default=None, blank=True)
    updated = models.DateTimeField(auto_now=True)
    post_time = models.DateTimeField(default=timezone.now)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    class Meta:
        ordering=['-post_time']
        
    def save(self, *args, **kwargs):
        if self.author and self.car and self.author != self.car.owner:
            raise ValidationError("You can only make a post for cars that you own.")
        super().save(*args, **kwargs)

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = f'{self.car.brand} {self.car.model}'
        super().save(*args, **kwargs)

    @property
    def num_likes(self):
        return self.liked_by.all().count()
    
    def __str__(self):
        return f"{self.title}"

class Review(models.Model):
    RATE_CHOICES = [(rate, rate) for rate in range(1, 6)]

    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='UserReviews')
    post = models.ForeignKey(Post, null=True, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(choices = RATE_CHOICES)
    content = models.TextField(blank=True)
    like = models.BooleanField(default=False)
    review_date = models.DateTimeField(default=timezone.now)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    class Meta:
        ordering=['-review_date']
            
    
    def __str__(self):
        return f"{self.user.username} reviewed {self.post.title}"



