from django import forms

class AddNewPostForm(forms.Form):
    post_title = forms.CharField(max_length=256)
    post_content = forms.CharField(widget=forms.Textarea())
