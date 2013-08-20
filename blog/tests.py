from django.test import TestCase

from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from blog.views import blog_main

class BlogTest(TestCase):

    def test_blog_url_resolves_to_blog_view(self):
        found = resolve('/blog')

        self.assertEqual(found.func, blog_main)

    def test_blog_url_returns_correct_html(self):
        request = HttpRequest() 
        response = blog_main(request) 

        expected_html = render_to_string('blog/main.html')
        self.assertEqual(response.content.decode(), expected_html)

    def test_blog_view_inherits_from_base_template(self):
        response = self.client.get('/blog')
        
        self.assertTemplateUsed(response, 'mainpage/base.html')
