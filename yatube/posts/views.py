from django.http import HttpResponse
from .models import Post, Group, Disk
from django.shortcuts import render, get_object_or_404, redirect
import datetime as dt
from django.core.mail import send_mail
from .forms import PostForm, ExchangeForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
# Create your views here.
User = get_user_model()

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
    if request.method =='POST':
        form = PostForm(request.POST)
        if not form.is_valid():
            return render(request,"new.html", {'form': form})
        form.instance.author = request.user
        form.save()
        return redirect('/')
    form = PostForm()
    return render(request,"new.html", {'form': form})


def group_posts(request, slug):
    if slug == 'none':
        group = None  
    else:
        group = get_object_or_404(Group, slug = slug) 
    posts = Post.objects.filter(group=group)[:12]
    return render(request, "group.html",{"group": group, "posts": posts})


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


def profile(request, username):
    for author in User.objects.all():
        if author.username == username:
            post_list = Post.objects.filter(author=User.objects.get(username=username))
            paginator = Paginator(post_list, 10)
            page_number = request.GET.get('page')
            page = paginator.get_page(page_number)
            return render(request, 'profile.html', {"page":page, "paginator": paginator, 'author': author})
    return HttpResponse('User is not found')

 
def post_view(request, username, post_id):
    for author in User.objects.all():
        if author.username == username:
            post = get_object_or_404(Post, id = post_id)
            return render(request, 'post.html', {'post':post,'author':author})
    return HttpResponse('User is not finded')

@login_required()
def post_edit(request, username, post_id):
    if request.user != User.objects.get(username=username):
        return HttpResponse('Ошибка доступа')
    if request.method =='POST':
        form = PostForm(request.POST)
        if not form.is_valid():
            return render(request,"new.html", {'form': form})
        post = Post.objects.get(id = post_id)
        post.text = form.cleaned_data['text']
        post.group = form.cleaned_data['group']
        post.save()
        return redirect('/')
    form = PostForm()
    return render(request,"new.html", {'form': form, 'method': 'edit'})
