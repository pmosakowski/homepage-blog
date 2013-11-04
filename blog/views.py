from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from blog.forms import AddNewPostForm
from blog.models import Post

def blog_main(request):
    return render(request, 'blog/main.html')

def new_post(request):
    if request.method == 'POST': 
        form = AddNewPostForm(request.POST) # A form bound to the POST data
        
        Post.objects.create(
                title=request.POST['post_title'],
                content=request.POST['post_content'])
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            #return render(request, 'blog/main.html', 
            #        {'posts': 
            #            {'title': request.POST['post_title'],
            #             'content': form.cleaned_data['post_content']}
            #        }
            #)
            return HttpResponseRedirect('/blog') # Redirect after POST
    else:
        form = AddNewPostForm() # An unbound form

    return render(request, 'blog/new-post.html', 
            {'form': form})
