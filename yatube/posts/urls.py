from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name = 'index'),
    path('new/', views.new_post, name = 'new_post'),
    path('latest/', views.latest, name = 'latest'),
    path('group/<slug:slug>', views.group_posts, name = 'group'),
    path("exchange/", views.Exchange, name = 'exchange'),
]
