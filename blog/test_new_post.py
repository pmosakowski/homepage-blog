from django.test import TestCase
from django.http import HttpRequest
from django.utils import timezone as tz

from django.core.urlresolvers import resolve
from django.template.loader import render_to_string

# user authentication
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from .models import Post
from .views import new_post
from .forms import AddNewPostForm

class NewPostTest(TestCase):
    def setUp(self):
        self.request = HttpRequest()
        # create user and log in
        User.objects.create_user('John Silver','j.silver@gmail.com','grog')
        self.user_credentials = {'username':'John Silver','password': 'grog'}
        self.user = authenticate(**self.user_credentials)
        self.request.user = self.user
        # post data for submission
        self.post_data = {
            'post_title': 'A new post title!!',
            'post_content': 'Some post content here.',
            'post_publication_date': '2012-01-15 17:00:00',
            'post_publish': 'True',
            'post_tags': 'programming web',
            'post_category': 'Tutorials',
        }

    def test_cannot_post_without_logging_in(self):
        self.client.logout()
        response = self.client.get('/blog/new-post')
        # we are not logged in and should get redirected
        self.assertRedirects(response,'/login?next=/blog/new-post',status_code=302)

    def test_new_post_url_resolves_to_new_post_view(self):
        found = resolve('/blog/new-post')

        self.assertEqual(found.func, new_post)

    def test_new_post_view_returns_correct_html(self):
        self.client.login(**self.user_credentials)
        response = self.client.get('/blog/new-post')

        # use same context as previous request
        expected_html = render_to_string('blog/new-post.html',response.context)

        self.assertEqual(response.content.decode(), expected_html)

    def test_new_post_view_inherits_from_blog_template(self):
        self.client.login(**self.user_credentials)
        response = self.client.get('/blog/new-post')

        self.assertTemplateUsed(response, 'blog/main.html')

    def test_new_post_view_returns_a_form(self):
        expected_html = render_to_string('blog/new-post.html',
                                {'form': AddNewPostForm()})

        self.assertIn('<form ', expected_html)
        self.assertIn('type="submit"', expected_html)

    def test_new_post_view_displays_POST_data(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST.update(self.post_data)

        expected_html = render_to_string('blog/new-post.html',
                            {'form' : AddNewPostForm(request.POST)})

        self.assertIn(self.post_data['post_title'], expected_html)
        self.assertIn(self.post_data['post_content'], expected_html)

    def test_new_post_view_redirects_on_submission(self):
        self.client.login(**self.user_credentials)
        response = self.client.post('/blog/new-post', self.post_data)

        # do we redirect to /blog ?
        self.assertEqual(302, response.status_code)
        self.assertRegex(response._headers.get('location')[1],
                r"^https?://[-\w]*/blog$")

    def test_new_post_view_saves_posts(self):
        self.request.method = 'POST'
        self.request.POST.update(self.post_data)

        self.assertEqual(Post.objects.all().count(), 0)
        new_post(self.request)
        self.assertEqual(Post.objects.all().count(), 1)

        post = Post.objects.all()[0]

        self.assertEqual(self.post_data['post_title'], post.title)
        self.assertEqual(self.post_data['post_content'], post.content)
        self.assertEqual(self.post_data['post_publication_date'], post.publication_date.strftime('%Y-%m-%d %H:%M:%S'))
        self.assertEqual(True, post.publish)
        self.assertEqual(self.post_data['post_tags'], post.tags)
        self.assertEqual(self.post_data['post_category'], str(post.category))

    def test_new_post_view_doesnt_save_empty_posts(self):
        self.request.method = 'POST'
        self.request.POST['post_title'] = ''
        self.request.POST['post_content'] = ''

        self.assertEqual(Post.objects.all().count(), 0)
        new_post(self.request)
        self.assertEqual(Post.objects.all().count(), 0)
