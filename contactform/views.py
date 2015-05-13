from django.shortcuts import render
from django.views.generic.edit import FormView

from .forms import ContactForm
# Create your views here.
class ContactFormView(FormView):
    form_class = ContactForm
