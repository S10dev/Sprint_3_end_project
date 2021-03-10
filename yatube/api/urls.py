from django.urls import path
from . import views
from rest_framework.authtoken import views as auth_views

urlpatterns =[
    path('posts/', views.get_post, name = 'get_post_api'),
    path('posts/<int:id>/', views.api_posts_detail, name = 'api_posts_detail'),
    #path('hello/', views.Hello.as_view(), name = 'hello'),
]


urlpatterns += [
    path('api-token-auth/', auth_views.obtain_auth_token)
]