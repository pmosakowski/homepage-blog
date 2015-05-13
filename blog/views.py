from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import django.utils.timezone as dtz
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from django.contrib.auth.decorators import login_required

from blog.forms import AddNewPostForm
from blog.models import Post, Category, title_to_link

def blog_main(request):
    posts = Post.objects.filter(publish=True,publication_date__lt=dtz.now())

    return render(request, 'blog/main.html', {'posts': posts})

@login_required
def new_post(request):
    if request.method == 'POST': 
        form = AddNewPostForm(request.POST) # A form bound to the POST data
        
        if form.is_valid(): # All validation rules pass
            Post.objects.create(
                    author=request.user,
                    title=form.cleaned_data['post_title'],
                    content=form.cleaned_data['post_content'],
                    link=title_to_link(form.cleaned_data['post_title']),
                    publication_date=form.cleaned_data['post_publication_date'],
                    publish=form.cleaned_data['post_publish'],
                    category=Category.get(form.cleaned_data['post_category']),
                    tags=form.cleaned_data['post_tags'],
            )
            return HttpResponseRedirect('/blog') # Redirect after POST
    else:
        form = AddNewPostForm() # An unbound form

    return render(request, 'blog/new-post.html', 
            {'form': form})

def view_post(request,post_link):
    post = Post.objects.get(link=post_link)

    return render(request, 'blog/view-post.html',{'post':post})

class CategoryDetailView(DetailView):
    model = Category
    context_object_name = 'category'
    slug_field = 'link'

    def get_context_data(self, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        context['posts'] = Category.objects.get(link=context['category'].link).post_set.all()
        return context

class CategoryListView(ListView):
    model = Category
