from django.test import TestCase
from django.core.urlresolvers import resolve
from .views import CategoryDetailView

class CategoryViewTest(TestCase):
    def test_url_resolves_to_correct_view(self):
        view = resolve('/blog/category/programming/') 
        view2 = resolve('/blog/category/programming') 

        self.assertEqual(CategoryDetailView.as_view().__name__, view.func.__name__)
        self.assertEqual(view2.func.__name__, view.func.__name__)
