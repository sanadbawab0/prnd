from django.contrib import admin
from car import models  
# Register your models here.
admin.site.register(models.Car)
admin.site.register(models.Tag)
admin.site.register(models.TechAndSafetyFeatures)
admin.site.register(models.PositiveAspect)
admin.site.register(models.NegativeAspect)
admin.site.register(models.PriceHistory)
admin.site.register(models.Review)
admin.site.register(models.ImageModel)
