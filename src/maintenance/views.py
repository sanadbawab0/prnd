from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers import *
from car.utils import cars_data 
# Create your views here.
@api_view(['GET'])
def get_maintenance_centers(request):
    if request.method == 'GET':
        maintenance_centers = MaintenanceCenter.objects.all()
        maintenance_centers_serializer = MaintenanceCenterSerializer(maintenance_centers, many=True)
    return Response (maintenance_centers_serializer.data)
    
@api_view(['GET'])
def get_maintenance_center(request,pk):
    if request.method == 'GET':
        maintenance_center = MaintenanceCenter.objects.get(id=pk)
        maintenance_centers_serializer = MaintenanceCenterSerializer(maintenance_center)
    return Response (maintenance_centers_serializer.data)
    
@api_view(['POST','GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def add_maintenance_center(request):
    if request.method == 'GET':
        brands = cars_data['Make'].unique()
        
        data = {
        'brands': brands }
        
    if request.method == 'POST' and request.user.is_authenticated:
        serializer = MaintenanceCenterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(data)
    

@api_view(['PUT'])
@permission_classes([IsAuthenticatedOrReadOnly])
def edit_maintenance_center(request, pk):
    maintenance_center = MaintenanceCenter.objects.get(id=pk)

    if request.method == 'PUT' and request.user.is_authenticated:
        serializer = EditMaintenanceCenterSerializer(instance=maintenance_center, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE', 'GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def delete_maintenance_center(request, pk):
    try:
        maintenance_center = MaintenanceCenter.objects.get(id=pk)
    except MaintenanceCenter.DoesNotExist:
        return Response({'message': 'Maintenance Center not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        maintenance_center_serializer = MaintenanceCenterSerializer(maintenance_center)  
        return Response(maintenance_center_serializer.data)
    
    if request.method == 'DELETE' and request.user.is_authenticated:
        maintenance_center.delete()
        return Response({'message': 'Maintenance Center deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
 