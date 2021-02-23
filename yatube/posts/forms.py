from django.contrib.auth import get_user_model
from django import forms
from .models import Group


class PostForm(forms.Form):
    choices = Group.objects.all()
    a = ((m,m) for m in choices)
    group = forms.ChoiceField(choices = a, required = False)
    text = forms.CharField(max_length=200)