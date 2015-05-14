from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from .forms import ContactForm
# Create your views here.
class ContactFormView(FormView):
    form_class = ContactForm
    template_name = 'contactform/contact.html'
    success_url = '/contact/thanks'

class ThanksView(TemplateView):
    template_name = 'contactform/thanks.html'
