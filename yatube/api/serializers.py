from rest_framework import serializers
from posts.models import Post



class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['text', 'pub_date', 'author', 'id'] 
        read_only_fields = ['author']
