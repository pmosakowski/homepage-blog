from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import django.utils.timezone as dtz

from django.contrib.auth.decorators import login_required

from blog.forms import AddNewPostForm
from blog.models import Post, title_to_link

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
                    category=form.cleaned_data['post_category'],
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
