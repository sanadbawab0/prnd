from django.shortcuts import redirect
from django.urls import reverse
from .models import *
from news_and_articles.models import NewsAndArticles
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from .serializers import *
from news_and_articles.serializers import NewsAndArticlesSerilizer
from django.db.models import Min, Max, Avg
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .utils import *
from .forms import *
from .filters import *

# Create your views here.

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_cars(request):
    if request.method == 'GET':
        car = Car.objects.all()
        car_serializer = ViewCarSerializer(car, many = True)
    return Response(car_serializer.data)

@api_view(['GET', 'POST'])
def home_page(request):
    if request.method == 'POST':

        min_price = request.data.get('min_price')
        max_price = request.data.get('max_price')
        query_params = []
        if min_price is not None:
            query_params.append(f'min_price={min_price}')
        if max_price is not None:
            query_params.append(f'max_price={max_price}')

        if query_params:
            query_string = '&'.join(query_params)
            redirect_url = f'{reverse("all_ads_page")}?{query_string}'
        return redirect(redirect_url)
        
    if request.method == 'GET':
        
        news = NewsAndArticles.objects.all()
        brands = cars_data['Make'].unique()
        body_types = [choice[1] for choice in BODY_CHOICES]
        car_tags = Tag.objects.exclude(tags__isnull=True).values_list('name', flat=True).distinct()
        car_fuel_types = [choice[1] for choice in FUEL_CHOICES]

        news_serializer = NewsAndArticlesSerilizer(news, many=True)
        
        data = {
            "brands": list(brands),
            "body_types": list(body_types),
            "tags": list(car_tags),
            "fuel_types": car_fuel_types,
            "news": news_serializer.data,
        }

        return Response(data)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def get_car_details(request, pk):
    try:
            car = Car.objects.get(id=pk)
            review = car.get_reviews
            positive_aspects = car.positive_aspects.all()
            negative_aspects = car.negative_aspects.all()
            price_history = PriceHistory.objects.filter(car=car).order_by('date')
            price_stats = PriceHistory.objects.filter(car=car).aggregate(
                min_price=Min('price'),
                max_price=Max('price'),
                avg_price=Avg('price')
            )
            other_cars = Car.objects.exclude(id=pk)
            competitor_cars = Car.objects.filter(brand__iexact=car.brand).exclude(id=car.id)

    except Car.DoesNotExist:
            return Response({'error': 'Car not found'}, status=status.HTTP_404_NOT_FOUND)
        

    if request.method == 'GET':

        car_serializer = CarDetailsSerializer(car)
        positive_aspects_serializer = PositiveAspectSerializer(positive_aspects, many=True)
        negative_aspects_serializer = NegativeAspectSerializer(negative_aspects, many=True)
        price_serializer = PriceHistorySerializer(price_history, many=True)
        price_stats_serializer = PriceStatisticsSerializer(price_stats)
        car_ads_serializer = CarAdsSerializer(other_cars, many = True)
        competitor_cars_serializer = CompetitorCarSerializer(competitor_cars, many=True)
        review_serializer = CarReviewSerializer(review, many = True)
        
        data = {
            "car_data": car_serializer.data,
            "positive_aspects": positive_aspects_serializer.data,
            "negative_aspects": negative_aspects_serializer.data,
            "price_stats": price_stats_serializer.data,
            "price_history": price_serializer.data,
            "cars_ads": car_ads_serializer.data,
            "competitor_cars": competitor_cars_serializer.data,
            "review" :review_serializer.data,
     }
        
    if request.method == 'POST' and request.user.is_authenticated :
        user_profile = request.user.profile
        serializer = CarReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['user'] = user_profile

            serializer.save(post=car)  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(data)

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def all_ads_page(request):
    brands = cars_data['Make'].unique()
    body_types = [choice[1] for choice in BODY_CHOICES]
    transmission_type = [choice[1] for choice in TRANSMISSION_CHOICES]
    car_fuel_types = [choice[1] for choice in FUEL_CHOICES]
    color = [choice[1] for choice in COLOR_CHOICES]
    condition = [choice[1] for choice in CONDITION_CHOICES]
    custom = [choice[1] for choice in CUSTOM_CHOICES]

    selected_brand = request.GET.get('brand')

    if selected_brand:
        brands = selected_brand
        models = Car.objects.filter(brand=selected_brand).values_list('model', flat=True).distinct()
    else:
        models = []

    queryset = Car.objects.all()
    filter_set = CarFilter(request.GET, queryset=queryset)
    
    if filter_set.is_valid():
        queryset = filter_set.qs
        if not queryset.exists():
            return Response({'message': 'No cars found'}, status=200)
    else:
        return Response({'error': 'Invalid filter parameters'}, status=400)
        
    
    page = request.GET.get('page')
    custom_range, cars = paginatePosts(request, queryset, 10, page)
    car_Serializer = ViewCarSerializer(cars, many=True)

    
    data = {
        'brands': brands,
        'models': models,
        'body_types': body_types,
        'transmission_types': transmission_type,
        'fuel_types': car_fuel_types,
        'colors': color,
        'conditions': condition,
        'customs': custom,
        'cars': car_Serializer.data,
        'custom_range':list(custom_range),
        }

    if request.method == 'POST' and request.user.is_authenticated:
        car_id = request.data.get('id')
        try:
            car = Car.objects.get(pk=car_id)
        except Car.DoesNotExist:
            return Response({'message': 'Car not found'}, status=404)

        profile = request.user.profile
        if car in profile.favorite_cars.all():
            profile.favorite_cars.remove(car)
            return Response({'message': 'Car removed from favorites'}, status=200)
        else:
            profile.favorite_cars.add(car)
            return Response({'message': 'Car added to favorites'}, status=201)


    return Response(data)

@api_view(['GET'])
def advanced_search(request):
     if request.method=='GET':
        
        brands = cars_data['Make'].unique()
        models = cars_data['Model'].unique()
        body_types = [choice[1] for choice in BODY_CHOICES]
        transmission_type = [choice[1] for choice in TRANSMISSION_CHOICES]
        car_fuel_types = [choice[1] for choice in FUEL_CHOICES]
        color = [choice[1] for choice in COLOR_CHOICES]
        condition = [choice[1] for choice in CONDITION_CHOICES]
        custom = [choice[1] for choice in CUSTOM_CHOICES]

        selected_brand = request.GET.get('brand')

        if selected_brand:
            brands = selected_brand
            models = Car.objects.filter(brand=selected_brand).values_list('model', flat=True).distinct()
        else:
            models = []

        data = {
        'brands': brands,
        'models': models,
        'body_types': body_types,
        'transmission_types': transmission_type,
        'fuel_types': car_fuel_types,
        'colors': color,
        'conditions': condition,
        'customs': custom,
        }
        return Response(data)


@api_view(['POST','GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def add_car(request):
    if request.method == 'GET':
        brands = cars_data['Make'].unique()
        body_types = [choice[1] for choice in BODY_CHOICES]
        transmission_type = [choice[1] for choice in TRANSMISSION_CHOICES]
        car_fuel_types = [choice[1] for choice in FUEL_CHOICES]
        color = [choice[1] for choice in COLOR_CHOICES]
        condition = [choice[1] for choice in CONDITION_CHOICES]
        custom = [choice[1] for choice in CUSTOM_CHOICES]
        data = {
        'brands': brands,

        'body_types': body_types,
        'transmission_types': transmission_type,
        'fuel_types': car_fuel_types,
        'colors': color,
        'conditions': condition,
        'customs': custom,
        }
    if request.method == 'POST' and request.user.is_authenticated:
        serializer = CarSerializer(data=request.data)

        if serializer.is_valid():
            serializer.validated_data['owner'] = request.user.profile
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(data)

@api_view(['PUT'])
@permission_classes([IsAuthenticatedOrReadOnly])
def edit_car(request, pk):
    
    try:
        car = Car.objects.get(id=pk)
    except Car.DoesNotExist:
        return Response({'message': 'Car not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT' and request.user.is_authenticated:
        serializer = CarEditSerializer(instance=car, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE', 'GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def delete_car(request, pk):
    try:
        car = Car.objects.get(id=pk)
    except Car.DoesNotExist:
        return Response({'message': 'Car not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        car_serializer = ViewCarSerializer(car)  
        return Response(car_serializer.data)
    
    if request.method == 'DELETE' and request.user.is_authenticated:
        car.delete()
        return Response({'message': 'Car deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


    




