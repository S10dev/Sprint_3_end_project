from django.http import HttpResponse
from .models import Post, Group, Disk
from django.shortcuts import render, get_object_or_404, redirect
import datetime as dt
from django.core.mail import send_mail
from .forms import PostForm, ExchangeForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
# Create your views here.

def index(request):
    if request.method =='POST':
        req = request.POST['search'].replace(' ','+')
        return redirect(f'/?q={req}')
    elif request.method =='GET':
        keyword = request.GET.get("q", None)
        if keyword:
            posts = Post.objects.select_related("author").filter(text__contains=keyword)
            count = posts.count()
        else:
            posts = None
        if not 'count' in locals():
            count = 0
        return render(request,"index.html", {"posts": posts, "keyword": keyword, 'count': count})

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