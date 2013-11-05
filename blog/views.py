from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from blog.forms import AddNewPostForm
from blog.models import Post

def blog_main(request):
    posts = Post.objects.all()

    return render(request, 'blog/main.html', {'posts': posts})

def new_post(request):
    if request.method == 'POST': 
        form = AddNewPostForm(request.POST) # A form bound to the POST data
        
        if form.is_valid(): # All validation rules pass
            Post.objects.create(
                    title=form.cleaned_data['post_title'],
                    content=form.cleaned_data['post_content'])
            
            return HttpResponseRedirect('/blog') # Redirect after POST
    else:
        form = AddNewPostForm() # An unbound form

    return render(request, 'blog/new-post.html', 
            {'form': form})
