from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length = 200)
    slug = models.SlugField(unique = True)
    description = models.TextField(default = "")

    def __str__(self):
        return str(self.title)


class Post(models.Model):
    text = models.TextField(verbose_name ='Текст')
    pub_date = models.DateTimeField("date published",auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, related_name="posts",
        blank = True, null = True, verbose_name ='Группа')

    def __str__(self):
        return str(self.text)
    

    class Meta:
        ordering = ['-pub_date']


class Disk(models.Model):
    artist = models.CharField(max_length=100)
    new_request = models.CharField(max_length=100)
    date = models.DateTimeField('date requested', auto_now_add=True)

    def __str__(self):
        return self.artist


    class Meta:
        ordering = ['-date']