from django.test import TestCase
from django.template import Template, Context

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

        TEMPLATE = Template("{% load blog_tags %} {% category_list %}")
        result = TEMPLATE.render(Context({}))

        self.assertInHTML('<h1> Categories </h1>', result)
        self.assertInHTML("<li><a href='/blog/category/programming/'>Programming</a></li>", result)
        self.assertInHTML("<li><a href='/blog/category/business/'>Business</a></li>", result)
        self.assertInHTML("<li><a href='/blog/category/system-administration/'>System administration</a></li>", result)
