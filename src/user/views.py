from rest_framework.decorators import api_view, permission_classes,authentication_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from .serializers import *
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
import jwt
from django.conf import settings
from django.contrib.auth import get_user_model

@api_view(['POST'])
@permission_classes([AllowAny])
def Register(request):
    if request.method == 'POST':
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            new_user = serializer.save()

            refresh = RefreshToken.for_user(new_user)
            access_token = str(refresh.access_token)

            response = Response(status=status.HTTP_201_CREATED)
            response.set_cookie(key='access_token', value=access_token, httponly=True)

            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def Login(request):
    email = request.data.get('email', None)
    user_password = request.data.get('password', None)

    if not user_password:
        return Response({'error': 'A user password is needed.'}, status=status.HTTP_400_BAD_REQUEST)

    if not email:
        return Response({'error': 'An user email is needed.'}, status=status.HTTP_400_BAD_REQUEST)

    user_instance = authenticate(username=email, password=user_password)

    if not user_instance:
        return Response({'error': 'User not found.'}, status=status.HTTP_401_UNAUTHORIZED)

    if user_instance.is_active:
        refresh = RefreshToken.for_user(user_instance)
        access_token = str(refresh.access_token)

        response = Response()
        response.set_cookie(key='access_token', value=access_token, httponly=True)
        response.data = {
            'access_token': access_token
        }
        return response

    return Response({'message': 'Something went wrong.'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([AllowAny])
def UserView(request):
    user_token = request.COOKIES.get('access_token')

    if not user_token:
        return Response({'error': 'Unauthenticated user.'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        payload = jwt.decode(user_token, settings.SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return Response({'error': 'Unauthenticated user.'}, status=status.HTTP_401_UNAUTHORIZED)

    user_model = get_user_model()
    user = user_model.objects.filter(id=payload['user_id']).first()
    
    if not user:
        return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    user_serializer = CustomUserSerializer(user)
    return Response(user_serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def Logout(request):
    user_token = request.COOKIES.get('access_token', None)
    
    if user_token:
        response = Response({'message': 'Logged out successfully.'}, status=status.HTTP_200_OK)
        response.delete_cookie('access_token')
        return response
    
    return Response({'message': 'User is already logged out.'}, status=status.HTTP_200_OK)
    
@api_view(['GET', 'PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def EditProfile(request):

    user = request.user

    if request.method == 'GET':
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = EditProfileSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)