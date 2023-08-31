from django_filters.rest_framework import DjangoFilterBackend

class CarFilter(DjangoFilterBackend):
    def filter_queryset(self, request, queryset, view):
        brand = request.GET.get('brand')
        model = request.GET.get('model')
        body_type = request.GET.get('body_type')
        release_year = request.GET.get('release_year')
        transmission_type = request.GET.get('transmission_type')
        fuel_type = request.GET.get('fuel_type')
        color = request.GET.get('color')
        condition = request.GET.get('custom')
        custom = request.GET.get('condition')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        
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
    

