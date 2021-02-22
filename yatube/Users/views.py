#  импортируем CreateView, чтобы создать ему наследника
from django.views.generic import CreateView
from django.http import HttpResponse
import datetime as dt
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.conf import settings
from .models import Disk
#  функция reverse_lazy позволяет получить URL по параметру "name" функции path()
#  берём, тоже пригодится
from django.urls import reverse_lazy

#  импортируем класс формы, чтобы сослаться на неё во view-классе
from .forms import CreationForm, ExchangeForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy("login") #  где login — это параметр "name" в path()
    template_name = "signup.html"
    
def year(request):
    current_year = dt.datetime.now().year
    return {"current_year": current_year}


def Exchange(request):
    if request.method == 'POST':
        form = ExchangeForm(request.POST)
        artist = request.POST.get('artist')
        if not Disk.objects.filter(artist=artist).exists():
            return HttpResponse('Нам такой артист не нужен')

        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            title = form.cleaned_data['title']
            artist = form.cleaned_data['artist']
            genre = form.cleaned_data['genre']
            price = form.cleaned_data['price']
            comment = form.cleaned_data['comment']
            

            #send_mail('Обмен диском', f'Добрый день! Меня зовут {name} и я хочу обменяться с вами диском '
            #f'артиста {artist} жанра {genre} с названием {title} по цене {price}. Комментарий: {comment}. Моя почта для связи: {email}',
            #'from@mail.ru', ['to@mail.ru'], fail_silently=False)

            return HttpResponse('Спасибо!')

        else:
            return HttpResponse("Invalid data")

        return render(request, 'Exchange.html', {'form': form})
    else:
        form = ExchangeForm()
        return render(request, 'Exchange.html', {'form': form})
