from django.test import TestCase, Client

from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.contrib.auth.models import User

from .models import Category, Post
from .views import CategoryDetailView, CategoryListView

class CategoryDetailViewTest(TestCase):
    def setUp(self):
        author = User.objects.create_user(
                    'user1',
                    'user@example.com',
                    'pass'
        )
        self.post = Post.objects.create(
            author=author,
            title='This is a programming article',
            content='Article content',
            publish=True,
            category=Category.get('Programming'),
        )
        Post.objects.create(
            author=author,
            title='This is a knitting tutorial',
            content='Tutorial content',
            publish=True,
            category=Category.get('Knitting'),
        )

    def test_url_resolves_to_correct_view(self):
        view = resolve('/blog/category/programming/') 
        view2 = resolve('/blog/category/programming') 

        self.assertEqual(CategoryDetailView.as_view().__name__, view.func.__name__)
        self.assertEqual(view2.func.__name__, view.func.__name__)

    def test_url_returns_correct_html(self):
        request = HttpRequest()
        request.method = "GET"

        response = CategoryDetailView.as_view()(request, slug='programming').render()
        render_dict = {
                'category': Category.get('Programming'),
                'posts': Category.get('Programming').post_set.all(),
        }
        expected_html = render_to_string('blog/category_detail.html', render_dict)

        self.assertEqual(expected_html, response.content.decode())

        # check diplayed fields
        self.assertContains(response, 'Programming')

        # displays first post
        self.assertContains(response, 'This is a programming article')

        # doesn't display post belonging to another category
        self.assertNotContains(response, 'This is a knitting tutorial')

    def test_view_inherits_correct_templates(self):
        c = Client()
        response = c.get('/blog/category/programming/')

        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'blog/main.html')
        self.assertTemplateUsed(response, 'blog/post.html')

class CategoryListViewTest(TestCase):

    def test_url_resolves_to_correct_view(self):
        view = resolve('/blog/categories/')
        view2 = resolve('/blog/categories')

        self.assertEqual(CategoryListView.as_view().__name__, view.func.__name__)
        self.assertEqual(view.func.__name__, view2.func.__name__)
