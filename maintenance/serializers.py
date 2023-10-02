from rest_framework import serializers

from .models import *


class MaintenanceCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceCenter
        fields = '__all__'


class EditMaintenanceCenterSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255, required=False)
    contact_number = serializers.CharField(max_length=20, required=False)
    location = serializers.CharField(max_length=20, required=False)

    class Meta:
        model = MaintenanceCenter
        fields = '__all__'
