from rest_framework import serializers 

from .models import *
from maintenance.models import MaintenanceCenter


class CarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Car
        fields = ['id','owner','brand','model','release_year']

class CompetitorCarSerializer(serializers.ModelSerializer):
    review_average = serializers.ReadOnlyField()
    num_reviewers = serializers.ReadOnlyField()

    class Meta:
        model = Car
        fields = ['brand','model','price','horse_power','speed','fuel_mileage','review_average', 'num_reviewers']

class CarAdsSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = Car
        fields = ['username','title','brand','model','price']

    def get_username(self, obj):
        return obj.owner.username

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        exclude = ['id']

class TechAndSafetyFeaturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechAndSafetyFeatures
        exclude = ['id']

class MaintenanceCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceCenter
        fields = '__all__'

class PositiveAspectSerializer(serializers.ModelSerializer):
    class Meta:
        model = PositiveAspect
        fields = '__all__'

class NegativeAspectSerializer(serializers.ModelSerializer):
    class Meta:
        model = NegativeAspect
        fields = '__all__'

class InteriorImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = InteriorImage
        fields = ['interior_image']

class ExteriorImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExteriorImage
        fields = ['exterior_image']

class CarDetailsSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    maintenance_centers = MaintenanceCenterSerializer(many=True, read_only=True)
    tech_and_safety_features = TechAndSafetyFeaturesSerializer(many=True, read_only=True)
    maintenance_centers_count = serializers.ReadOnlyField()
    similar_cars_count = serializers.ReadOnlyField()
    review_average = serializers.ReadOnlyField()
    interior_images = InteriorImageSerializer(many=True)
    exterior_images = ExteriorImageSerializer(many=True)
    
    class Meta:
        model = Car
        fields = '__all__'
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        reordered_data = {}

        for field_name in self.fields.keys():
            if field_name not in ['tags', 'maintenance_centers', 'tech_and_safety_features']:
                reordered_data[field_name] = data[field_name]

        reordered_data['tags'] = data['tags']
        reordered_data['maintenance_centers'] = data['maintenance_centers']
        reordered_data['tech_and_safety_features'] = data['tech_and_safety_features']

        return reordered_data
    



class PriceHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceHistory
        fields = ['price','date']



class AllAdsSerializer(serializers.ModelSerializer):
     class Meta:
         model = Car
         fields = ['title','discription','image']



class CarReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['user']


class PriceStatisticsSerializer(serializers.Serializer):
    min_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    max_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    avg_price = serializers.DecimalField(max_digits=10, decimal_places=2)

class HomePageSerilizer(serializers.Serializer):
       class Meta:
           model =  Car
           fields = ['brands','body_types','tags','fuel_types']
        



