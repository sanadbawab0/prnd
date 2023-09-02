from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers import *

# Create your views here.

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def news_page(request):
    if request.method == "GET":
        article = NewsAndArticles.objects.all()
        serializer = NewsAndArticlesSerilizer(article, many=True)
        return Response(serializer.data)
    
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


#TODO GET POST 
#TODO EDIT POST
#TODO DELETE POST
