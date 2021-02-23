from django.contrib.auth import get_user_model
from django.forms import ModelForm
from .models import Group, Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = {'group', 'text'}