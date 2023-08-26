from django.contrib import admin
from news_and_articles import models

# Register your models here.

admin.site.register(models.NewsAndArticles)
admin.site.register(models.NewsAndArticlesReview)
