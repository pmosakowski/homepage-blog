from django import forms
from django.contrib.auth.models import User

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=256)
    message = forms.CharField(widget=forms.Textarea)
    contact_email = forms.EmailField(max_length=256)

    def send_email(self):
        contact = User.objects.get(username='contact')

        contact.email_user(
                self.cleaned_data['subject'],
                self.cleaned_data['message'],
                self.cleaned_data['contact_email'])
