from django.db import models
from django_countries.fields import CountryField
import uuid
from user.models import Profile
from maintenance.models import MaintenanceCenter
from django.utils import timezone
from django.db.models import Avg
import math
from .utils import *
# Create your models here.




current_year = timezone.now().year

class Car(models.Model):
    id =  models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    owner = models.ForeignKey(Profile, null=True, on_delete=models.CASCADE, related_name='owned_cars')
    title = models.CharField(max_length = 200, blank = True)
    description = models.TextField(blank = True)
    brand = models.CharField(max_length=50, choices=BRAND_CHOICES)
    model = models.CharField('model', max_length=50)
    country = CountryField()
    release_year = models.PositiveIntegerField()
    engine_size = models.PositiveIntegerField(blank=True, null=True)
    fuel_type = models.CharField(max_length=20,choices=FUEL_CHOICES, blank=True, null=True)
    transmission_type = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES, blank=True, null=True)
    weight = models.PositiveIntegerField(blank=True, null=True, )
    horse_power = models.PositiveIntegerField(blank=True, null=True)
    speed = models.PositiveBigIntegerField(blank=True, null=True)
    fuel_mileage = models.PositiveIntegerField(blank=True, null=True)
    Odometer = models.PositiveIntegerField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, blank=True, null=True)
    custom = models.CharField(max_length=20, choices=CUSTOM_CHOICES, blank=True, null=True)
    body_type = models.CharField(max_length=20, choices = BODY_CHOICES, blank=True, null=True)
    color = models.CharField(max_length=10, blank=True, null=True, choices=COLOR_CHOICES)
    interior = models.TextField(blank=True ,null=True )
    exterior = models.TextField(blank=True ,null=True)
    performance = models.CharField(max_length=50, blank=True, null=True)
    performance_description = models.TextField(blank=True ,null=True)
    tags = models.ManyToManyField('Tag', related_name='tags', default=None, blank=True)
    tech_and_safety_features = models.ManyToManyField('TechAndSafetyFeatures', related_name='cars', blank=True, default = None)
    maintenance_centers = models.ManyToManyField(MaintenanceCenter, default=None, blank = True, related_name='maintenance_centers')
    updated = models.DateTimeField(auto_now=True)
    post_time = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(release_year__gte=1900) & models.Q(release_year__lte=current_year + 2), 
                name="valid_release_year"
            )
        ]
    
    def save(self, *args, **kwargs):
        if self.pk is not None:
            old_instance = Car.objects.get(pk=self.pk)
            if old_instance.price != self.price:
                PriceHistory.objects.create(car=self, price=self.price)
        super().save(*args, **kwargs)

    @property
    def get_reviews(self):
        return Review.objects.filter(post=self)

    @property
    def maintenance_centers_count(self):
        return self.maintenance_centers.count()
    

    @property
    def similar_cars_count(self):
        return Car.objects.filter(brand__iexact=self.brand, model__iexact=self.model).exclude(id=self.id).count()
    
    @property
    def review_average(self):
        average_rating = self.reviews.aggregate(Avg('rating'))['rating__avg']
        if average_rating is not None:
            return math.ceil(average_rating)
        return 0
    
    @property
    def num_reviewers(self):
        num_reviewers = self.reviews.values('user').distinct().count()
        return num_reviewers
    
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
    

class InteriorImage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='interior_images')
    interior_image = models.ImageField(upload_to=car_image_interior_path, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Interior Image {self.id} for {self.car}"

class ExteriorImage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='exterior_images')
    exterior_image = models.ImageField(upload_to=car_image_exterior_path, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Exterior Image {self.id} for {self.car}"

class Review(models.Model):
    RATE_CHOICES = [(rate, rate) for rate in range(1, 6)]

    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='UserReviews')
    post = models.ForeignKey(Car, null=True, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(choices = RATE_CHOICES)
    content = models.TextField(blank=True)
    review_date = models.DateTimeField(default=timezone.now)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    class Meta:
        ordering=['-review_date']
    
    def __str__(self):
        return f"{self.user.username} reviewed {self.post.title}"



