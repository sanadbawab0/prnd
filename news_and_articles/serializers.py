from rest_framework import serializers
from .models import *


class NewsAndArticlesSerilizer(serializers.ModelSerializer):
    class Meta:
        model = NewsAndArticles
        fields = '__all__'


class NewsAndArticlesReviewSerilizer(serializers.ModelSerializer):

    class Meta:
        model = NewsAndArticlesReview
        fields = '__all__'
        read_only_fields = ['user']
