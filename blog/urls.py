from django.conf.urls import patterns, include, url

urlpatterns = patterns('blog.views',
    url(r'^$', 'blog_main'),
    url(r'^/new-post$', 'new_post'),
)
