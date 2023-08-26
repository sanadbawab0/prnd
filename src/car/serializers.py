from rest_framework import serializers 
from .models import *

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'



class PriceHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceHistory
        fields = '__all__'


class PositiveAspectSerializer(serializers.ModelSerializer):
    class Meta:
        model = PositiveAspect
        fields = '__all__'

class NegativeAspectSerializer(serializers.ModelSerializer):
    class Meta:
        model = NegativeAspect
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class CarPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class CarReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


