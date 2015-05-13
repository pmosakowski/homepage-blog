from django.test import TestCase

from django.core.urlresolvers import resolve
# Create your tests here.

from .views import ContactFormView
from .forms import ContactForm

class ContactFormTest(TestCase):
    def test_url_resolves_to_contact_form_view(self):
        view = resolve('/contact/')

        self.assertEqual(ContactFormView.as_view().__name__, view.func.__name__)

    def test_contact_form_renders_required_fields(self):
        form_html = ContactForm().as_p()

        self.assertIn('id_subject', form_html)
        self.assertIn('id_message', form_html)
        self.assertIn('id_contact_email', form_html)
