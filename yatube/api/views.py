from django.shortcuts import render
from .serializers import PostSerializer
from django.http import JsonResponse
from pprint import pprint
from django.shortcuts import get_object_or_404
from posts.models import Post, User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404



@api_view(['GET', 'POST'])
def get_post(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = PostSerializer(data=request.data) 
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def api_posts_detail(request, id):
    post = get_object_or_404(Post, id = id)
    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)
    elif (request.method == 'PUT' or request.method == 'PATCH') and post.author == request.user:
        serializer = PostSerializer(post, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE' and post.author == request.user:
        post.delete()
        return Response({'status': 'deleted'})
    else:
        return Response(status = status.HTTP_403_FORBIDDEN)

