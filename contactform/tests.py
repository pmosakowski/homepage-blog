from django.test import TestCase, Client
from django.core import mail
from django.contrib.auth.models import User

from django.template.loader import render_to_string
from django.core.urlresolvers import resolve
from django.http import HttpRequest
# Create your tests here.

from .views import ContactFormView, ThanksView
from .forms import ContactForm

class ContactFormTest(TestCase):
    def setUp(self):
        User.objects.create_user('contact', 'contact@example.com','kibbles', first_name='Mister', last_name='Contact')

    def test_url_resolves_to_contact_form_view(self):
        view = resolve('/contact/')

        self.assertEqual(ContactFormView.as_view().__name__, view.func.__name__)

    def test_view_renders_correct_html(self):
        request = HttpRequest()
        request.method = "GET"

        response = ContactFormView.as_view()(request).render()
        expected_html = render_to_string('contactform/contact.html',{'form':ContactForm()})

        self.assertEqual(expected_html, response.content.decode())

    def test_view_renders_form_html(self):
        form_html = ContactForm().as_p()

        request = HttpRequest()
        request.method = "GET"
        response = ContactFormView.as_view()(request).render()

        self.assertIn(form_html, response.content.decode())

    def test_contact_form_renders_required_fields(self):
        form_html = ContactForm().as_p()

        self.assertIn('id_subject', form_html)
        self.assertIn('id_message', form_html)
        self.assertIn('id_contact_email', form_html)

    def test_contact_form_uses_main_application_template(self):
        response = Client().get('/contact')

        self.assertTemplateUsed(response, 'mainpage/main.html')

    def test_contact_form_redirects_on_success(self):
        contact_request = {
                'subject': 'Some subject',
                'message': 'A message goes here',
                'contact_email': 'mrpopo@example.com',
        }

        response = Client().post('/contact', contact_request)
        self.assertRedirects(response, '/contact/thanks')

    def test_contact_form_sends_an_email(self):
        contact_request = {
                'subject': 'Some subject',
                'message': 'A message goes here',
                'contact_email': 'mrpopo@example.com',
        }

        self.assertEqual(0, len(mail.outbox))
        response = Client().post('/contact', contact_request)
        self.assertEqual(1, len(mail.outbox))
        self.assertEqual(contact_request['subject'], mail.outbox[0].subject)

class ThanksViewTest(TestCase):
    def test_url_resolves_to_thanks_view(self):
        view = resolve('/contact/thanks')

        self.assertEqual(ThanksView.as_view().__name__, view.func.__name__)

    def test_url_renders_correct_html(self):
        response = Client().get('/contact/thanks')
        expected_html = render_to_string('contactform/thanks.html')

        self.assertEqual(expected_html, response.content.decode())
        self.assertTemplateUsed(response, 'mainpage/main.html')
