from rest_framework import serializers 

from .models import *

class NewsAndArticlesSerilizer(serializers.ModelSerializer):
    class Meta:
        model = NewsAndArticles
        fields = '__all__'


