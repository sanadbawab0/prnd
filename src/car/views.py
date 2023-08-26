from .models import *
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
#from .utils import get_image_url
from .serializers import *
from django.db.models import Min, Max, Avg

# Create your views here.
@api_view(['GET'])
def get_cars(request):
    car = Car.objects.all()
    if request.method == 'GET':
        car_serializer = CarSerializer(car, many = True)
    return Response(car_serializer.data)



@api_view(['GET'])
def get_car_details(request, pk):
    try:
        car = Car.objects.get(id=pk)
        review = car.get_reviews
        positive_aspects = car.positive_aspects.all()
        negative_aspects = car.negative_aspects.all()
        #similar_posts = Car.objects.filter(brand__iexact=car.brand, model__iexact=car.model).exclude(id=car.id)
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
        #similar_posts_serializer = SimilarPostSerializer(similar_posts, many=True)
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

    return Response(data)



