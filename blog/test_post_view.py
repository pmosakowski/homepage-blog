from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils import timezone as tz

from django.contrib.auth.models import User

from .models import Post, Category,title_to_link
from .views import  view_post

class PostViewTest(TestCase):
    def setUp(self):
        self.author_credentials = {
                'username': 'mrauthor',
                'password': 'pass',
        }

        self.author = User.objects.create_user(
                self.author_credentials['username'],
                'author@writers.com',
                self.author_credentials['password'],
                first_name='Mr',
                last_name='Author'
        )

        self.post_object = Post.objects.create(
                title='A new post title!!',
                author = self.author,
                content = '##Subheading\nSome post content here.',
                link = title_to_link('A new post title!!'),
                publication_date = tz.make_aware(tz.datetime(2012,2,15,17,0,0)),
                tags = 'programming web',
                category = Category.get('tutorials')
        )

    def test_post_is_assigned_a_link_name(self):
        post = Post.objects.all()[0]
        self.assertEqual(post.link, 'a-new-post-title')

    def test_post_url_resolves_to_post_view(self):
        found = resolve('/blog/post/%s/' % self.post_object.link)

        self.assertEqual(found.func, view_post)

    def test_blog_url_returns_correct_html(self):
        response = view_post(HttpRequest(), self.post_object.link)

        expected_html = render_to_string('blog/view-post.html', {'post': self.post_object})
        self.assertEqual(response.content.decode(), expected_html)

    def test_post_view_renders_markdown(self):
        response = view_post(HttpRequest(), self.post_object.link)
        self.assertContains(response, '<h2>Subheading</h2>', html=True)

    def test_post_view_uses_correct_templates(self):
        response = self.client.get('/blog/post/a-new-post-title/')
        self.assertTemplateUsed(response, 'blog/main.html')
        self.assertTemplateUsed(response, 'blog/view-post.html')
        self.assertTemplateUsed(response, 'blog/post.html')

    def test_post_has_an_individual_link(self):
        response = self.client.get('/blog/post/a-new-post-title/')
        self.assertIn('A new post title!!', response.content.decode())

    def test_post_displays_publication_date(self):
        response = self.client.get('/blog/post/a-new-post-title/')
        self.assertIn('2012-02-15', response.content.decode())

    def test_post_displays_author(self):
        response = self.client.get('/blog/post/a-new-post-title/')
        self.assertIn('by Mr Author', response.content.decode())

    def test_post_displays_category(self):
        response = self.client.get('/blog/post/%s/' % self.post_object.link)
        self.assertContains(response, 'tutorials')

    def test_blog_view_displays_new_post_link_only_to_logged_in_users(self):
        # not logged in
        self.client.logout()
        response = self.client.get('/blog/post/%s/' % self.post_object.link)
        self.assertNotContains(response, '<a href="/blog/new-post">New post',
                status_code=200, html=True)

        # logged in
        self.client.login(**self.author_credentials)
        response = self.client.get('/blog/post/%s/' % self.post_object.link)
        self.assertContains(response, '<a href="/blog/new-post">New post',
                status_code=200, html=True)
