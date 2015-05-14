from django import forms
from django.core import mail

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=256)
    message = forms.CharField(widget=forms.Textarea)
    contact_email = forms.EmailField(max_length=256)

    def send_email(self):
        mail.send_mail(
                self.cleaned_data['subject'],
                self.cleaned_data['message'],
                self.cleaned_data['contact_email'],
                ['admin@example.com'],
                fail_silently = False
        )
        pass
