import django_filters
from django_filters.rest_framework import FilterSet
from .models import *


class CarFilter(FilterSet):
    min_price = django_filters.NumberFilter(
        field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(
        field_name='price', lookup_expr='lte')

    class Meta:
        model = Car
        fields = ['brand', 'model', 'body_type',
                  'release_year', 'transmission_type', 'fuel_type',
                  'color', 'condition', 'custom']
