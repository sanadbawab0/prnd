from .models import *
from news_and_articles.models import NewsAndArticles
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from .serializers import *
from news_and_articles.serializers import NewsAndArticlesSerilizer
from django.db.models import Min, Max, Avg
from .utils import *
from .forms import *
from .filters import *
# Create your views here.

@api_view(['GET', 'POST'])
def home_page(request):
    if request.method == 'POST':
        min_price = request.data.get('min_price')
        max_price = request.data.get('max_price')
        request.session['min_price'] = min_price
        request.session['max_price'] = max_price
        queryset = Car.objects.all()
        filtered_queryset = CarFilterBackend().filter_queryset(request, queryset, None)  
        serializer = CarSerializer(filtered_queryset, many=True)
        return Response({"redirect": "all_ads_page", "filtered_cars": serializer.data})

    if request.method == 'GET':
        news = NewsAndArticles.objects.all()
        brands = cars_data['Make'].unique()
        body_types = [choice[1] for choice in BODY_CHOICES]
        car_tags = Tag.objects.exclude(tags__isnull=True).values_list('name', flat=True).distinct()
        car_fuel_types = Car.objects.exclude(fuel_type__isnull=True).values_list('fuel_type', flat=True).distinct()
        
        news_serializer = NewsAndArticlesSerilizer(news, many=True)
        
        data = {
            "brands": list(brands),
            "body_types": list(body_types),
            "tags": list(car_tags),
            "fuel_types": car_fuel_types,
            "news": news_serializer.data,
        }

        return Response(data)


@api_view(['GET'])
def get_cars(request):
    if request.method == 'GET':
        car = Car.objects.all()
        car_serializer = CarSerializer(car, many = True)
    return Response(car_serializer.data)


@api_view(['GET', 'POST'])
def get_car_details(request, pk):
    form = ReviewForm()
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
        review_serializer = CarReviewSerializer(review, many = True)
        price_serializer = PriceHistorySerializer(price_history, many=True)
        price_stats_serializer = PriceStatisticsSerializer(price_stats)
        other_cars_serializer = CarAdsSerializer(other_cars, many = True)
        competitor_cars_serializer = CompetitorCarSerializer(competitor_cars, many=True)
        
        data = {
            "car_data": car_serializer.data,
            "positive_aspects": positive_aspects_serializer.data,
            "negative_aspects": negative_aspects_serializer.data,
            "review" :review_serializer.data,
            "price_stats": price_stats_serializer.data,
            "price_history": price_serializer.data,
            #"similar_posts": similar_posts_serializer.data,
            "other_cars": other_cars_serializer.data,
            "competitor_cars": competitor_cars_serializer.data,
     }
        
    if request.method == 'POST':
        serializer = CarReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user.profile, car=car)  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(data)

@api_view(['POST'])
def all_ads_page(request):
    form = CarFilterForm(request.data)
    if form.is_valid():
        queryset = Car.objects.all()  
        filtered_queryset = CarFilterBackend().filter_queryset(request, queryset, None)  
        serializer = CarSerializer(filtered_queryset, many=True)
        return Response(serializer.data)
    




