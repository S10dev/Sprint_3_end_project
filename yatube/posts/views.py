from django.http import HttpResponse
from .models import Post, Group
from django.shortcuts import render, get_object_or_404, redirect
import datetime as dt
# Create your views here.


def index(request):
    if request.method =='POST':
        req = request.POST['search'].replace(' ','+')
        return redirect(f'/?q={req}')
    elif request.method =='GET':
        keyword = request.GET.get("q", None)
        if keyword:
            posts = Post.objects.select_related("author").filter(text__contains=keyword)
        else:
            posts = None
         
        return render(request,"index.html", {"posts": posts, "keyword": keyword})





"""
def index(request):
    latest = Post.objects[:10]
    return render(request, "index.html", {"posts": latest} )


def group_posts(request, slug):
    group = get_object_or_404(Group, slug = slug)
    posts = Post.objects.filter(group=group)[:12]
    return render(request, "group.html",{"group": group, "posts": posts})
    """