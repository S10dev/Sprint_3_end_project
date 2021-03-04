from django.test import TestCase
from django.test import Client
from django.contrib.auth import get_user_model
from .models import Post
from django.urls import reverse
User = get_user_model()

# Create your tests here.


class Test1_2(TestCase):
    def setUp(self):
        self.username = 'fasjsakfhassHAjfgh'
        self.email = 'test@test.test'
        self.password = 'KHDjhfjhasjjJ2'
        self.c_nonlogged = Client()
        self.c_logged = Client()
        self.c_nonlogged.post('/auth/signup/', {'username': self.username,
                                            'email':self.email,
                                            'password1': self.password,
                                            'password2': self.password
                                            }, follow=True)
        self.c_logged.login(username=self.username, password =self.password)

    def test_1(self):
        response = self.c_nonlogged.get(reverse('profile', kwargs={'username':self.username}))
        self.assertEqual(response.status_code, 200)

    
    def test_2(self):
        user = User.objects.get(username=self.username)
        self.c_logged.post(reverse('new_post'), {'text':'TestStuff'}, follow=True)
        self.assertEqual(user.posts.get(text = 'TestStuff').author, user)


    def test_3(self):
        self.assertRedirects(self.c_nonlogged.get(reverse('new_post')), '/auth/login/?next=/new/', status_code=302, 
                            target_status_code=200, fetch_redirect_response=True)


    def test_4(self):
        text = "Test"
        self.c_logged.post(reverse('new_post'), {'text':text})
        page_index = self.c_logged.get(reverse('index'), follow=True).context['page']
        self.assertEqual(page_index[0].text, text)
        page_profile = self.c_logged.get(
            reverse('profile',
            kwargs = {
                'username':self.username
                }),
                follow = True).context['page']

        self.assertEqual(page_profile[0].text, text)
        post = self.c_logged.get(
            reverse('post', 
            kwargs = {
                'username':self.username,
                'post_id':Post.objects.get(text=text).id
                }),
            follow = True).context['post']
            
        self.assertEqual(post.text, text)


    def test_5(self):
        self.c_logged.post(reverse('new_post'), {'text':'not edited'})
        self.c_logged.post(
            reverse('post_edit',
            kwargs={
                'username':self.username,
                'post_id':Post.objects.get(text="not edited").id
                }
                ),
                {'text':'edited'}
            )
        text = "edited"
        page_index = self.c_logged.get(reverse('index'), follow=True).context['page']
        self.assertEqual(page_index[0].text, text)
        page_profile = self.c_logged.get(
            reverse('profile',
            kwargs = {
                'username':self.username
                }),
                follow = True).context['page']

        self.assertEqual(page_profile[0].text, text)
        post = self.c_logged.get(
            reverse('post', 
            kwargs = {
                'username':self.username,
                'post_id':Post.objects.get(text=text).id
                }),
            follow = True).context['post']
            
        self.assertEqual(post.text, text)

