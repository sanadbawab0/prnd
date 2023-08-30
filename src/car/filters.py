from rest_framework.filters import BaseFilterBackend

class CarFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        brand = request.data.get('brand')
        model = request.data.get('model')
        body_type = request.data.get('body_type')
        release_year = request.data.get('release_year')
        transmission_type = request.data.get('transmission_type')
        fuel_type = request.data.get('fuel_type')
        color = request.data.get('color')
        condition = request.data.get('custom')
        custom = request.data.get('condition')
        min_price = request.data.get('min_price')
        max_price = request.data.get('max_price')
        
        if brand:
            queryset = queryset.filter(brand=brand)
        if model:
            queryset = queryset.filter(model=model)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        if body_type:
            queryset = queryset.filter(body_type=body_type)
        if release_year:
            queryset = queryset.filter(release_year=release_year)
        if transmission_type:
            queryset = queryset.filter(transmission_type=transmission_type)
        if fuel_type:
            queryset = queryset.filter(fuel_type=fuel_type)
        if color:
            queryset = queryset.filter(color=color)
        if condition:
            queryset = queryset.filter(condition=condition)
        if custom:
            queryset = queryset.filter(custom=custom)
        return queryset
    

