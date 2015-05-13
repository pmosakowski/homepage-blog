from django.test import TestCase

from django.core.urlresolvers import resolve
# Create your tests here.

from .views import ContactFormView

class ContactFormTest(TestCase):
    def test_url_resolves_to_contact_form_view(self):
        view = resolve('/contact/')

        self.assertEqual(ContactFormView.as_view().__name__, view.func.__name__)
