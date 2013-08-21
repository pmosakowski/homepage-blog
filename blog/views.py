from django.shortcuts import render
from blog.forms import AddNewPostForm


def blog_main(request):
    return render(request, 'blog/main.html')

def new_post(request):
    form =  AddNewPostForm()

    return render(request, 'blog/new-post.html', 
            {'form': form})
