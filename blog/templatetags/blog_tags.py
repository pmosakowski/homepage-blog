from django.template import Library
from ..models import Category

register = Library()

@register.inclusion_tag('blog/category.html')
def category_list():
    categories = Category.objects.all()
    return {'categories': categories}
