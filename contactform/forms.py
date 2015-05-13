from django import forms

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=256)
    message = forms.CharField(widget=forms.Textarea)
    contact_email = forms.EmailField(max_length=256)
