from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from mainpage.views import main_page, about_page

class HomePageTest(TestCase):

    def test_root_url_resolves_to_main_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, main_page)

    def test_main_view_page_returns_correct_html(self):
        request = HttpRequest() 
        response = main_page(request) 

        expected_html = render_to_string('mainpage.html')
        self.assertEqual(response.content.decode(), expected_html)

    def test_main_view_inherits_base_template(self):
        response = self.client.get('/')
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'base.html')

    def test_main_view_displays_main_menu_template(self):
        response = self.client.get('/')
        
        self.assertTemplateUsed(response,'mainmenu.html')
    
    def test_main_menu_contains_about_link(self):
        response = self.client.get('/')
        self.assertContains(response, '<div id="main-menu"><a href="about">About',
                status_code=200, html=True)

    def test_about_url_resolves_to_main_page_view(self):
        found = resolve('/about')
        self.assertEqual(found.func, about_page)

    def test_about_view_page_returns_correct_html(self):
        request = HttpRequest() 
        response = about_page(request) 

        expected_html = render_to_string('about.html')
        self.assertEqual(response.content.decode(), expected_html)
