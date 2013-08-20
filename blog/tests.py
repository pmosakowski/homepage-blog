from django.test import TestCase
from django.core.urlresolvers import resolve

from blog.views import blog_main

class BlogTest(TestCase):

    def test_blog_url_resolves_to_blog_view(self):
        found = resolve('/blog')

        self.assertEqual(found.func, blog_main)
