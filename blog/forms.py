from django import forms
from django.core import validators


class TitleField(forms.CharField):
    default_error_messages = {
        'min_length': ('Title cannot be left empty.')
    }
    default_validators = [validators.MinLengthValidator(1)]


class AddNewPostForm(forms.Form):
    post_title = TitleField(max_length=512)
    post_content = forms.CharField(widget=forms.Textarea())
    post_publication_date = forms.DateTimeField()
    post_tags = forms.CharField(max_length=256)
    post_category = forms.CharField(max_length=256)
