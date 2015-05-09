from django.test import TestCase, Client
from django.contrib.auth.models import User

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

    def test_submitting_a_new_post(self):
        new_post =  {
                'post_title': 'Test title',
                'post_content': 'Some post content',
                'post_publication_date': '2015-04-20 13:10:00',
                'post_category': 'programming',
                'post_tags': 'python django',
        }

        c = Client()
        c.login(username = 'shheppard', password = 'somepass')
        response = c.post('/blog/new-post', new_post)
        self.assertRedirects(response, '/blog')

        post_link = Post.objects.all()[0].link
        response = c.get('/blog/%s/' % post_link)
        print(response.content.decode())
        # check if post displays all the elements
        for key in new_post:
            self.assertContains(response, new_post[key])
