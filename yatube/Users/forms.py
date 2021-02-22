from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms

User = get_user_model()


#  создадим собственный класс для формы регистрации
#  сделаем его наследником предустановленного класса UserCreationForm
class CreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        # укажем модель, с которой связана создаваемая форма
        model = User
        # укажем, какие поля должны быть видны в форме и в каком порядке
        fields = ("first_name", "last_name", "username", "email")


class ExchangeForm(forms.Form):
    pass
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    title = forms.CharField(max_length=100)
    artist = forms.CharField(max_length=40)
    genre = forms.ChoiceField(choices = ((1,"one") ,(2,"two")))
    price = forms.IntegerField(required = False)
    comment = forms.CharField(max_length=200, required = False)