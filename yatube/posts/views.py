from django.http import HttpResponse
from .models import Post, Group
from django.shortcuts import render, get_object_or_404
# Create your views here.


def index(request):
    latest = Post.objects[:10]
    return render(request, "index.html", {"posts": latest} )


def group_posts(request, slug):
    group = get_object_or_404(Group, slug = slug)
    posts = Post.objects.filter(group=group)[:12]
    return render(request, "group.html",{"group": group, "posts": posts})