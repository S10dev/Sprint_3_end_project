from django.http import HttpResponse
from .models import Post, Group, Disk, Comment, Follow
from django.shortcuts import render, get_object_or_404, redirect
import datetime as dt
from django.core.mail import send_mail
from .forms import PostForm, ExchangeForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.http import Http404
from django.urls import reverse
from django.views.decorators.cache import cache_page
# Create your views here.
User = get_user_model()


@cache_page(20, key_prefix='index_page')
def index(request):
    post_list = Post.objects.order_by('-pub_date').all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'index.html',
        {'page': page, 'paginator': paginator}
    )

@login_required()
def new_post(request):
    form = PostForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        form.instance.author = request.user
        form.save()
        return redirect('/')
    return render(request,"new.html", {'form': form})


def group_posts(request, slug):
    if slug == '404':
        group = None  
    else:
        group = get_object_or_404(Group, slug = slug) 
    posts = Post.objects.filter(group=group)
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, "group.html",{"group": group, "page": page, 'paginator':paginator})


def Exchange(request):
    if request.method == 'POST':
        form = ExchangeForm(request.POST)
        artist = request.POST.get('artist')
        if not Disk.objects.filter(artist=artist).exists():
            return HttpResponse('Нам такой артист не нужен')

        if not form.is_valid():
            return HttpResponse("Invalid data")

            
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        title = form.cleaned_data['title']
        artist = form.cleaned_data['artist']
        genre = form.cleaned_data['genre']
        price = form.cleaned_data['price']
        comment = form.cleaned_data['comment']
        send_email = form.cleaned_data['send_email']
        
        if send_email:
            send_mail('Обмен диском', f'Добрый день! Меня зовут {name} и я хочу обменяться с вами диском '
            f'артиста {artist} жанра {genre} с названием {title} по цене {price}. Комментарий: {comment}. Моя почта для связи: {email}',
            '', [''], fail_silently=False)
        
        Disk.objects.create(artist=artist, new_request=f'Добрый день! Меня зовут {name} и я хочу обменяться с вами диском '
        f'артиста {artist} жанра {genre} с названием {title} по цене {price}. Комментарий: {comment}. Моя почта для связи: {email}')

        return HttpResponse('Спасибо!')

        return render(request, 'Exchange.html', {'form': form})
    else:
        form = ExchangeForm()
        return render(request, 'Exchange.html', {'form': form})

@login_required()
def profile(request, username):
    author = get_object_or_404(User, username=username)
    post_list = author.posts.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    following = False
    if Follow.objects.filter(user = request.user, author = author):
        following = True
    return render(request, 'profile.html', {"page":page, "paginator": paginator, 'author': author, 'following': following})


def post_view(request, username, post_id):
    for author in User.objects.all():
        if author.username == username:
            post = get_object_or_404(Post, id = post_id)
            items = post.comment.all()
            form = CommentForm(request.POST or None)
            paginator = Paginator(items, 10)
            page_number = request.GET.get('page')
            page = paginator.get_page(page_number)
            return render(request, 'post.html', {'post':post, "paginator": paginator, 'page':page,
             'form':form, 'author':author, 'items':items})
    raise Http404


@login_required()
def post_edit(request, username, post_id):
    post = get_object_or_404(Post, id = post_id, author__username = username)
    if request.user.username != post.author.username:
        return redirect('post', username = username, post_id = post_id)
    form = PostForm(request.POST or None, files=request.FILES or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('post', username = username, post_id = post_id)
    return render(request,"new.html", {'form': form, 'edit': True, 'post':post})


def page_not_found(request, exception):
    return render(
        request, 
        "misc/404.html", 
        {"path": request.path}, 
        status=404
    )


def server_error(request):
    return render(request, "misc/500.html", status=500)


@login_required()
def add_comment(request, username, post_id):
    post = Post.objects.get(id = post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        form.instance.author = request.user
        form.instance.post = post
        form.save()
        return redirect('post', username=username, post_id=post_id)
    return redirect('post', username=username, post_id=post_id)


@login_required()
def follow_index(request):
    posts = Post.objects.filter(author__following__in=Follow.objects.filter(user=request.user))

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request,'follow.html', {'page': page, 'paginator': paginator, 'followid':True})


@login_required()
def profile_follow(request, username):
    if request.user.username == username:
        return redirect('profile', username=username)
    author = User.objects.get(username=username)
    if Follow.objects.filter(user=request.user, author=User.objects.get(username = username)):
        return redirect('profile', username=username)
    Follow.objects.create(user=request.user, author=author)
    return redirect('profile', username=username)


@login_required()
def profile_unfollow(request, username):
    author = User.objects.get(username=username)
    Follow.objects.get(user=request.user, author=author).delete()
    return redirect('profile', username=username)
