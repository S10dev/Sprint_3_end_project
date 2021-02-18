from django.http import HttpResponse
from .models import Post
from django.shortcuts import render 
# Create your views here.


def index(request):
    latest = Post.objects.order_by('-pub_date')[:10]
    return render(request, "index.html", {"posts": latest} )