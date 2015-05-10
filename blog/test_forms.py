from django.test import TestCase
from django.utils import timezone as tz

from blog.forms import AddNewPostForm

class NewPostFormTest(TestCase):
    def setUp(self):
        self.post_data = {
            'post_title': 'A new post title!!',
            'post_content': 'Some post content here.',
            'post_publication_date': tz.datetime(2012,3,15,17,0,0),
            'post_publish': True,
            'post_tags': 'programming web',
            'post_category': 'Tutorials'
        }

    def test_form_validation(self):
        form = AddNewPostForm(self.post_data)
        
        self.assertTrue(form.is_valid())
        self.assertEqual(True,{}==form.errors)

    def test_form_returns_correct_fields(self):
        form = AddNewPostForm().as_p()

        self.assertIn('id_post_title', form)
        self.assertIn('id_post_content', form)
        self.assertIn('id_post_publication_date', form)
        self.assertIn('id_post_publish' ,form)
        self.assertIn('id_post_tags', form)
        self.assertIn('id_post_category', form)

    def test_form_publish_checkbox_can_be_set(self):
        form = AddNewPostForm(self.post_data)
        self.assertTrue(form.is_valid())
        self.assertTrue(form.cleaned_data['post_publish'])
