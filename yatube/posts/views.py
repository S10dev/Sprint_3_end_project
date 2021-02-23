from django.http import HttpResponse
from .models import Post, Group
from django.shortcuts import render, get_object_or_404, redirect
import datetime as dt
from .forms import PostForm
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.conf import settings
# Create your views here.
User = get_user_model()

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


def new_post(request):
    if request.method =='POST':
        form = PostForm(request.POST)
        if form.is_valid():
            group = form.cleaned_data['group']
            if group == '':
                group = None
            else:
                group = Group.objects.get(title = group)
            text = form.cleaned_data['text']
            author_name = f'{request.user.username}'
            user = User.objects.get(username=author_name)
            Post.objects.create(text = text, author = user, group=group)

            return redirect('/latest/')



        return HttpResponse('not valid data')
    else:
        form = PostForm(request.POST)
        return render(request,"new.html", {'form': form})



def latest(request):
    latest = Post.objects.all()[:10]
    return render(request, "latest.html", {"posts": latest} )


"""

def group_posts(request, slug):
    group = get_object_or_404(Group, slug = slug)
    posts = Post.objects.filter(group=group)[:12]
    return render(request, "group.html",{"group": group, "posts": posts})
    """