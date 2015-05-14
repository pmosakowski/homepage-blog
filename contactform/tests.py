from django.test import TestCase, Client

from django.template.loader import render_to_string
from django.core.urlresolvers import resolve
from django.http import HttpRequest
# Create your tests here.

from .views import ContactFormView
from .forms import ContactForm

class ContactFormTest(TestCase):
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
