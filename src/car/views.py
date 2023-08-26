from .models import *
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
#from .utils import get_image_url
from .serializers import *

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
        #review =Review.objects.get(post=2)
    except Car.DoesNotExist:
        return Response({'error': 'Car not found'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        car_serializer = CarSerializer(car)
        #review_serializer = CarReviewSerializer(review)


    data = {
        "car_data": car_serializer.data,
        #"review" :review_serializer.data,

    }

    return Response(data)



