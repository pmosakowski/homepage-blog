from ..models import Category

def category_list():
    categories = Category.objects.all()
    return {'categories': categories}
