from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest

from mainpage.views import main_page

class HomePageTest(TestCase):

    def test_root_url_resolves_to_main_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, main_page)

    def test_main_view_page_returns_correct_html(self):
        request = HttpRequest() 
        response = main_page(request) 
        self.assertTrue(response.content.startswith(b'<html>'))
        self.assertIn(b'<title>Homepage</title>', response.content) 
        self.assertTrue(response.content.strip().endswith(b'</html>'))
