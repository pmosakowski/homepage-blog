from django.test import TestCase, Client

from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from .models import Category
from .views import CategoryDetailView

class CategoryViewTest(TestCase):
    def setUp(self):
        self.category = Category.get('Programming')

    def test_url_resolves_to_correct_view(self):
        view = resolve('/blog/category/programming/') 
        view2 = resolve('/blog/category/programming') 

        self.assertEqual(CategoryDetailView.as_view().__name__, view.func.__name__)
        self.assertEqual(view2.func.__name__, view.func.__name__)

    def test_url_returns_correct_html(self):
        request = HttpRequest()
        request.method = "GET"

        response = CategoryDetailView.as_view()(request, slug='programming').render()
        expected_html = render_to_string('blog/category_detail.html')

        self.assertEqual(expected_html, response.content.decode())

    def test_view_inherits_main_blog_template(self):
        c = Client()
        response = c.get('/blog/category/programming/')

        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'blog/main.html')
