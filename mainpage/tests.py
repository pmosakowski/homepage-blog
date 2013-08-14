from django.core.urlresolvers import resolve
from django.test import TestCase
from mainpage.views import main_page

class HomePageTest(TestCase):

        def test_root_url_resolves_to_main_page_view(self):
            found = resolve('/')
            self.assertEqual(found.func, main_page)
