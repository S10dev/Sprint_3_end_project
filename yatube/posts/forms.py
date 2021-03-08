from django.contrib.auth import get_user_model
from django.forms import ModelForm
from django import forms
from .models import Group, Post, Comment


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = {'group', 'text', 'image'}


class CommentForm(ModelForm):
    text = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Comment
        fields = {'text'}


class ExchangeForm(forms.Form):
    pass
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    title = forms.CharField(max_length=100)
    artist = forms.CharField(max_length=40)
    genre = forms.ChoiceField(choices = ((1,"one") ,(2,"two")))
    price = forms.IntegerField(required = False)
    comment = forms.CharField(max_length=200, required = False)
    send_email = forms.BooleanField(required=False)