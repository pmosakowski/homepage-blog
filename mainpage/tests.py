from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

# for auth tests
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from mainpage.views import main_page, about_page, login_page, logout_page
from mainpage.forms import LoginForm

class HomePageTest(TestCase):

    def test_root_url_resolves_to_main_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, main_page)

    def test_main_view_page_returns_correct_html(self):
        request = HttpRequest() 
        response = main_page(request) 

        expected_html = render_to_string('mainpage/main.html')
        self.assertEqual(response.content.decode(), expected_html)

    def test_main_view_inherits_base_template(self):
        response = self.client.get('/')
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'mainpage/base.html')

    def test_main_view_links_to_css(self):
        response = self.client.get('/')
        
        self.assertContains(response, 'mainpage/css/main.css',
                status_code=200)

    def test_main_view_displays_main_menu_template(self):
        response = self.client.get('/')
        
        self.assertTemplateUsed(response,'mainpage/mainmenu.html')
    
    def test_main_menu_contains_about_link(self):
        response = self.client.get('/')
        self.assertContains(response, '<a href="about">About',
                status_code=200, html=True)

    def test_main_menu_contains_blog_link(self):
        response = self.client.get('/')
        self.assertContains(response, '<a href="blog">Blog',
                status_code=200, html=True)

    def test_main_page_contains_login_link(self):
        response = self.client.get('/')
        self.assertContains(response, '<a href="/login">Log in',
                status_code=200, html=True)

    def test_main_page_contains_logout_link(self):
        # set up and login
        User.objects.create_user('John Rambo','rambo@firstblood.vt','rpg')
        login_data = { 
                'username': 'John Rambo', 
                'password': 'rpg'
        }
        self.client.login(**login_data)

        # proper test
        response = self.client.get('/')
        self.assertContains(response, '<a href="/logout">Log out',
                status_code=200, html=True)

class AboutPageTest(TestCase):
    def test_about_url_resolves_to_about_page_view(self):
        found = resolve('/about')
        self.assertEqual(found.func, about_page)

    def test_about_view_page_returns_correct_html(self):
        request = HttpRequest() 
        response = about_page(request) 

        expected_html = render_to_string('mainpage/about.html')
        self.assertEqual(response.content.decode(), expected_html)

class LoginPageTest(TestCase):
    def setUp(self):
        User.objects.create_user('Juan Ramirez','juan@mexicocity.mx','tequila')
        self.correct_login_data = { 
                'username': 'Juan Ramirez', 
                'password': 'tequila'
        }
        self.incorrect_login_data = { 
                'username': 'Juan Ramirez', 
                'password': 'tequila2000'
        }

    def test_login_url_resolves_to_login_page_view(self):
        found = resolve('/login')
        self.assertEqual(found.func, login_page)

    def test_login_page_view_returns_correct_html(self):
        request = HttpRequest()
        response = login_page(request)

        expected_html = render_to_string('mainpage/login.html',
                {'form':LoginForm()})
        self.assertEqual(response.content.decode(), expected_html)

    def test_login_page_view_inherits_base_template(self):
        response = self.client.get('/login')
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'mainpage/base.html')

    def test_login_page_view_displays_login_form(self):
        response = login_page(HttpRequest())
        login_form = LoginForm()
        
        self.assertContains(response, login_form.as_p())

    def test_login_page_has_required_elements(self):
        response = login_page(HttpRequest())

        self.assertContains(response, '<input id="id_username" name="username" type="text"/>', html=True)
        self.assertContains(response, '<input id="id_password" name="password" type="password"/>', html=True)
        self.assertContains(response, '<input id="id_submit" type="submit" value="Login"/>', html=True)

    def test_login_page_redirects_on_correct_login(self):
        response = self.client.post('/login', self.correct_login_data)

        self.assertRedirects(response,'/blog', status_code=302)

    def test_framework_can_authenticate(self):
        user = authenticate(**self.correct_login_data)

        self.assertNotEqual(None,user)

    def test_login_view_can_log_user_in(self):
        response = self.client.post('/login', self.correct_login_data)
        response = self.client.get('/')

        self.assertContains(response, 'Juan Ramirez')

    def test_login_view_displays_error_on_incorrect_login(self):
        response = self.client.post('/login', self.incorrect_login_data)

class LogoutViewTest(TestCase):
    def setUp(self):
        User.objects.create_user('Juan Ramirez','juan@mexicocity.mx','tequila')
        self.correct_login_data = { 
                'username': 'Juan Ramirez', 
                'password': 'tequila'
        }

        self.client.login(**self.correct_login_data)

    def test_about_url_resolves_to_main_page_view(self):
        found = resolve('/logout')
        self.assertEqual(found.func, logout_page)

    def test_can_log_out(self):
        response = self.client.get('/')
        self.assertContains(response, 'Juan Ramirez')

        self.client.get('/logout')
        response = self.client.get('/')
        self.assertNotContains(response, 'Juan Ramirez')
        self.assertContains(response, 'Log in')
