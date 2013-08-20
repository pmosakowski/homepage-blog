from django.shortcuts import render

def blog_main(request):
    return render(request, 'blog/main.html')

def new_post(request):
    return render(request, 'blog/new-post.html')
