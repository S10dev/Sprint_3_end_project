from django.http import HttpResponse
from .models import Post, Group
from django.shortcuts import render, get_object_or_404, redirect
import datetime as dt
from .forms import PostForm
from django.contrib.auth.decorators import login_required
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

@login_required()
def new_post(request):
    if request.method =='POST':
        form = PostForm(request.POST)
        if not form.is_valid():
            return render(request,"new.html", {'form': form})
        form.instance.author = request.user
        form.save()
        return redirect('/')
    form = PostForm()
    return render(request,"new.html", {'form': form})



def latest(request):
    latest = Post.objects.all()[:10]
    return render(request, "latest.html", {"posts": latest} )


def group_posts(request, slug):
    group = get_object_or_404(Group, slug = slug)
    if slug == '3':
        group = None   
    posts = Post.objects.filter(group=group)[:12]
    return render(request, "group.html",{"group": group, "posts": posts})