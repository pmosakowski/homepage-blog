from django.test import TestCase

from .templatetags.blog_tags import category_list
from .models import Category

class CategoryListTagView(TestCase):
    def setUp(self):
        Category.get('Programming')
        Category.get('Business')
        Category.get('System administration')
        Category.get('programming')

    def test_category_view_tags_renders_correct_html(self):
        db_cat_count = Category.objects.all().count()
        tag_cat_count = category_list()['categories'].count()

        self.assertEqual(db_cat_count, tag_cat_count)
        self.assertEqual(3, tag_cat_count)
