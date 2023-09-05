from rest_framework.decorators import api_view, permission_classes,authentication_classes
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

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
        serializer = MyTokenObtainPairSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            token = serializer.validated_data['access']
            return Response({'access_token': token}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def UserView(request):
    user = request.user
    serializer = CustomUserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def Logout(request):
    try:
        refresh_token = request.data.get('refresh_token')

        refresh_token_obj = RefreshToken(refresh_token)
        refresh_token_obj.blacklist()

        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': 'Unable to log out.'}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def EditProfile(request):
    if request == 'PUT':
        user = request.user
        serializer = EditProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
    return Response(serializer.data)