from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.http import HttpRequest

from django.utils.timezone import localtime

from .views import new_post
from .models import Post

class TestIntegration(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
                'shheppard',
                email = 'shep@example.com',
                password = 'somepass',
                first_name = 'John',
                last_name = 'Shepard',
        )

        self.new_post =  {
                'post_title': 'Test title',
                'post_content': 'Some post content',
                'post_publication_date': '2015-04-20 13:10:00',
                'post_category': 'programming',
                'post_tags': 'python django',
        }

    def test_creating_new_model_from_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST = self.new_post
        request.user = self.user

        new_post(request)

        post = Post.objects.all()[0]
        self.assertEquals(self.new_post['post_title'], post.title)
        self.assertEquals(self.new_post['post_content'], post.content)
        self.assertEquals(self.new_post['post_publication_date'], localtime(post.publication_date).strftime('%Y-%m-%d %H:%M:%S'))
        self.assertEquals(self.new_post['post_category'], str(post.category))
        self.assertEquals(self.new_post['post_tags'], post.tags)

    def test_submitting_a_new_post(self):
        c = Client()
        c.login(username = 'shheppard', password = 'somepass')
        response = c.post('/blog/new-post', self.new_post)
        self.assertRedirects(response, '/blog')

        post_link = Post.objects.all()[0].link
        response = c.get('/blog/%s/' % post_link)
        # check if post displays all the elements
        for key in self.new_post:
            if key == 'post_publication_date':
                self.assertContains(response, self.new_post['post_publication_date'].split()[0])
            else:
                self.assertContains(response, self.new_post[key])
