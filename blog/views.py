from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from blog.forms import AddNewPostForm


def blog_main(request):
    return render(request, 'blog/main.html')

def new_post(request):
    if request.method == 'POST': 
        form = AddNewPostForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            return HttpResponse(request.POST['post_title'] +
                                request.POST['post_content'])
            #return HttpResponseRedirect('/blog') # Redirect after POST
    else:
        form = AddNewPostForm() # An unbound form

    return render(request, 'blog/new-post.html', 
            {'form': form})
