from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers import *
from car.models import Car
from car.serializers import ViewCarSerializer

# Create your views here.

@api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticatedOrReadOnly])
def news_page(request):
    if request.method == "GET":
        article = NewsAndArticles.objects.all()
        car = Car.objects.all()
        article_serializer = NewsAndArticlesSerilizer(article, many=True)
        car_serializer = ViewCarSerializer(car, many = True)
        data = {
            "news and articles": article_serializer.data ,  
            "cars": car_serializer.data   
        }
        return Response(data)
    
    elif request.method == 'POST' and request.user.is_authenticated:
        action = request.data.get('action')  

        if action == 'add_to_favorites':
            article_id = request.data.get('id')
            try:
                article = NewsAndArticles.objects.get(pk=article_id)
            except NewsAndArticles.DoesNotExist:
                return Response({'message': 'Article not found'}, status=status.HTTP_404_NOT_FOUND)

            profile = request.user.profile
            if article in profile.favorite_posts.all():
                profile.favorite_posts.remove(article)
                return Response({'message': 'Article removed from favorites'}, status=status.HTTP_200_OK)
            else:
                profile.favorite_posts.add(article)
                return Response({'message': 'Article added to favorites'}, status=status.HTTP_201_CREATED)
        
        elif action == 'create_post':
            serializer = NewsAndArticlesSerilizer(data=request.data)
             
            if serializer.is_valid():
                serializer.validated_data['author'] = request.user.profile
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response({'message': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def article(request,pk):
    article = NewsAndArticles.objects.get(id=pk) 
    review = article.get_reviews
    if request.method == "GET":
        news_and_article_serializer = NewsAndArticlesSerilizer(article)
        review_serializer = NewsAndArticlesReviewSerilizer(review,many=True)
        data = {
            'news_and_article': news_and_article_serializer.data,
            'review': review_serializer.data,
        }
    if request.method == 'POST' and request.user.is_authenticated:
        user_profile = request.user.profile
        serializer = NewsAndArticlesReviewSerilizer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user_profile, news_article=article)  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(data)
    
@api_view(['PUT'])
@permission_classes([IsAuthenticatedOrReadOnly])
def edit_article(request,pk):
    try:
        article = NewsAndArticles.objects.get(id=pk)
    except NewsAndArticles.DoesNotExist:
        return Response({'message': 'Article not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT' and request.user.is_authenticated:
        serializer = NewsAndArticlesSerilizer(instance=article, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE', 'GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def delete_article(request, pk):
    try:
        article = NewsAndArticles.objects.get(id=pk)
    except NewsAndArticles.DoesNotExist:
        return Response({'message': 'article not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        car_serializer = NewsAndArticlesSerilizer(article)  
        return Response(car_serializer.data)
    
    if request.method == 'DELETE' and request.user.is_authenticated:
        article.delete()
        return Response({'message': 'article deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
