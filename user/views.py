from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from car.serializers import ViewCarSerializer
from news_and_articles.serializers import NewsAndArticlesSerilizer
from car.models import Car
from news_and_articles.models import NewsAndArticles


@api_view(['POST'])
@permission_classes([AllowAny])
def Register(request):
    if request.method == 'POST':
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def Login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = authenticate(email=email, password=password)

    if user is not None:
        serializer = MyTokenObtainPairSerializer(
            data=request.data, context={'request': request})

        if serializer.is_valid():
            token = serializer.validated_data['access']
            return Response({'access_token': token}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def UserProfile(request):
    user = request.user
    user_profile = request.user.profile
    profile = Profile.objects.get(user=user)

    user_data = {
        "profile_image": user_profile.profile_image.url,
        "num_followers": user_profile.followers.count(),
        "num_posts": user_profile.owned_cars.count() + user_profile.author.count(),
    }

    user_serializer = CustomUserSerializer(user, many=False)

    user_cars = Car.objects.filter(owner=profile)
    user_posts = NewsAndArticles.objects.filter(author=profile)

    car_serializer = ViewCarSerializer(user_cars, many=True)
    article_serializer = NewsAndArticlesSerilizer(user_posts, many=True)
    favorite_serializer = Favoriteserializer(user_profile)
    data = {

        'user': [user_serializer.data, user_data],
        'cars': car_serializer.data,
        'articles': article_serializer.data,
        'favorites': favorite_serializer.data
    }

    return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def Logout(request):
    try:
        refresh_token = request.data.get('access')
        print(f"Received refresh_token: {refresh_token}")
        refresh_token_obj = RefreshToken(refresh_token)
        refresh_token_obj.blacklist()
        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
    except Exception as e:
        print(f"Error during logout: {str(e)}")
        return Response({'error': 'Unable to log out.'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def EditProfile(request):
    if request == 'PUT':
        user = request.user
        serializer = EditProfileSerializer(
            user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
    return Response(serializer.data)


@api_view(['GET'])
def get_profiles(request):
    profiles = Profile.objects.all()
    serializer = ProfileSerializer(profiles, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def ViewOtherProfile(request, profile_id):
    try:
        user = Profile.objects.get(id=profile_id)
    except Profile.DoesNotExist:
        return Response({'message': 'Profile not found'}, status=404)

    if request.method == 'GET':

        user_data = {
            "username": user.user.username,
            "profile_image": user.profile_image.url,
            "num_followers": user.followers.count(),
            "num_posts": user.owned_cars.count() + user.author.count(),
        }

        ads = user.author.all()
        car = user.owned_cars.all()

        article_serializer = NewsAndArticlesSerilizer(ads, many=True)
        car_serializer = ViewCarSerializer(car, many=True)

        data = {
            "user": user_data,
            "article": article_serializer.data,
            "car": car_serializer.data
        }

        return Response(data, status=200)

    if request == 'POST' and request.user.is_authenticated:
        if user == request.user.profile:
            return Response({'error': 'You cannot follow/unfollow yourself'}, status=status.HTTP_400_BAD_REQUEST)

        if user.followers.filter(id=request.user.profile.id).exists():
            user.followers.remove(request.user.profile)
            return Response({'message': 'Unfollowed successfully'}, status=status.HTTP_200_OK)
        else:
            user.followers.add(request.user.profile)
            return Response({'message': 'Followed successfully'}, status=status.HTTP_200_OK)
