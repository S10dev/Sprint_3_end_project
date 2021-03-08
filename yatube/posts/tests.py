from django.test import TestCase
from django.test import Client
from django.contrib.auth import get_user_model
from .models import Post, Group, Follow
from django.urls import reverse
import random as rand
import time
from django.core.cache import cache
User = get_user_model()

# Create your tests here.


class Test1_2(TestCase):
    def setUp(self):
        self.c_nonlogged = Client()
        self.c_logged = Client()
        self.user = User.objects.create(username='ssss', password = '12345')
        self.c_logged.force_login(self.user)
    #После регистрации пользователя создается его персональная страница (profile)
    def test_1(self):
        response = self.c_nonlogged.get(reverse('profile', kwargs={'username':self.user.username}))
        self.assertEqual(response.status_code, 302)

    #Авторизованный пользователь может опубликовать пост (new)
    def test_2(self):
        self.c_logged.post(reverse('new_post'), {'text':'TestStuff'}, follow=True)
        self.assertEqual(self.user.posts.get(text = 'TestStuff').author, self.user)

    #Неавторизованный посетитель не может опубликовать пост (его редиректит на страницу входа)
    def test_3(self):
        self.assertRedirects(self.c_nonlogged.get(reverse('new_post')), '/auth/login/?next=/new/', status_code=302, 
                            target_status_code=200, fetch_redirect_response=True)

    #После публикации поста новая запись появляется на главной странице сайта (index), 
    # на персональной странице пользователя (profile), и на отдельной странице поста (post)
    def test_4(self):
        text = "Test"
        self.c_logged.post(reverse('new_post'), {'text':text})
        cache.clear()
        page_index = self.c_logged.get(reverse('index'), follow=True).context['page']
        self.assertEqual(page_index[0].text, text)
        page_profile = self.c_logged.get(
            reverse('profile',
            kwargs = {
                'username':self.user.username
                }),
                follow = True).context['page']

        self.assertEqual(page_profile[0].text, text)
        post = self.c_logged.get(
            reverse('post', 
            kwargs = {
                'username':self.user.username,
                'post_id':Post.objects.get(text=text).id
                }),
            follow = True).context['post']
            
        self.assertEqual(post.text, text)

    #Авторизованный пользователь может отредактировать свой пост 
    # и его содержимое изменится на всех связанных страницах
    def test_5(self):
        self.c_logged.post(reverse('new_post'), {'text':'not edited'})
        self.c_logged.post(
            reverse('post_edit',
            kwargs={
                'username':self.user.username,
                'post_id':Post.objects.get(text="not edited").id
                }
                ),
                {'text':'edited'}
            )
        text = "edited"
        cache.clear()
        page_index = self.c_logged.get(reverse('index'), follow=True).context['page']
        self.assertEqual(page_index[0].text, text)
        page_profile = self.c_logged.get(
            reverse('profile',
            kwargs = {
                'username':self.user.username
                }),
                follow = True).context['page']

        self.assertEqual(page_profile[0].text, text)
        post = self.c_logged.get(
            reverse('post', 
            kwargs = {
                'username':self.user.username,
                'post_id':Post.objects.get(text=text).id
                }),
            follow = True).context['post']
            
        self.assertEqual(post.text, text)

    #возвращает ли сервер код 404, если страница не найдена.
    def test_6(self):
        response = self.c_logged.get('/dsadhfuahsjdnajjfhjasnjd/')
        self.assertEqual(response.status_code, 404)


class ImgTests(TestCase):
    def setUp(self):
        self.c = Client()
        self.user = User.objects.create(username='12322', password='12332')
        self.c.force_login(self.user)
        with open('posts/111.png','rb') as img:
            self.post = self.c.post(
                reverse('new_post'),
                {'text': 'post with image', 'image': img}
                )

    #проверяют, что срабатывает защита от загрузки файлов не-графических форматов
    def test_7(self):
        with self.assertRaises(IndexError) as context:
            with open('posts/apps.py','rb') as img:
                self.post = self.c.post(
                    reverse('new_post'),
                    {'text': 'post with image', 'image': img}
                    )
                Post.objects.all()[1]

    #проверяют страницу конкретной записи с картинкой: на странице есть тег <img>
    #проверяют, что на главной странице, на странице профайла и 
    # на странице группы пост с картинкой отображается корректно, с тегом <img>
    def test_8(self):
        urls = [
            self.c.get(
                reverse('post', kwargs = {
                    'username':self.user.username, 'post_id':1
                    })
                ),
            self.c.get(
                reverse('profile', kwargs = {
                    'username':self.user.username
                    })
                ),
            self.c.get(reverse('group', kwargs = {'slug':404}))
        ]
        for url in urls:
            response = url
            self.assertContains(response,'<img', count = 1)
    

    #Напишите тесты, которые проверяют работу кэша.
    def test_9(self):
        self.c.post(reverse('new_post'), {'text':'Тест кэша'})
        response = self.c.get(reverse('index'))
        self.c.post(reverse('new_post'), {'text':'авфыв'})
        response = self.c.get(reverse('index'))
        self.assertNotContains(response, 'авфыв')

    #Авторизованный пользователь может подписываться 
    # на других пользователей и удалять их из подписок.
    def test_10(self):
        following = User.objects.create(username='dka', password= 'ssadasd')
        self.assertEqual(Follow.objects.filter(id =1).exists(), 0)
        self.c.get(reverse('profile_follow', kwargs = {'username': following.username}))
        self.assertEqual(Follow.objects.filter(id =1).exists(), 1)
        self.c.get(reverse('profile_unfollow', kwargs = {'username': following.username}))
        self.assertEqual(Follow.objects.filter(id =1).exists(), 0)

    #Новая запись пользователя появляется в ленте тех, 
    # кто на него подписан и не появляется в ленте тех, кто не подписан на него.
    def test_11(self):
        following = User.objects.create(username='dka', password= 'ssadasd')
        follower2 = User.objects.create(username='follower2', password='ssadasd')
        cfollower2 = Client()
        cfollower2.force_login(follower2)
        self.c.get(reverse('profile_follow', kwargs = {'username': following.username}))
        Post.objects.create(text = 'Тестовая вещь', author = following)
        response = self.c.get(reverse('follow_index'))
        self.assertContains(response,'Тестовая вещь')
        response = cfollower2.get(reverse('follow_index'))
        self.assertNotContains(response,'Тестовая вещь')


    #Только авторизированный пользователь может комментировать посты.
    def test_12(self):
        post = Post.objects.create(text = 'Тестовое письмо', author = self.user)
        self.c.post(reverse(
            'add_comment',
            kwargs = {'username':post.author.username,'post_id':post.id}), {'text':'вфывыафыва'}
            )
        response = self.c.get(reverse('post', kwargs = {'username':post.author.username,'post_id':post.id}))
        self.assertContains(response, 'вфывыафыва')
        cn = Client()
        cn.post(reverse(
            'add_comment',
            kwargs = {'username':post.author.username,'post_id':post.id}), {'text':'non_auth'}
            )
        response = cn.get(reverse('post', kwargs = {'username':post.author.username,'post_id':post.id}))
        self.assertNotContains(response, 'non_auth')


        
