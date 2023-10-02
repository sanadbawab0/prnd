from django.db import models
import pandas as pd
import uuid
# Create your models here.
data = pd.read_csv("Data.csv")
unique_makes = data["Make"].unique()
unique_makes.sort()

class MaintenanceCenter(models.Model):

    BRAND_CHOICES = [(make, make) for make in unique_makes]

    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    brand = models.CharField(max_length=50, null=True, choices=BRAND_CHOICES) 
    contact_number = models.CharField(max_length=20)
    description = models.TextField(blank=True ,null=True)
    website = models.URLField(blank=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    

        
    def __str__(self):
        return f"{self.name} - {self.brand}"
