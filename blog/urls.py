from django.conf.urls import patterns, include, url

urlpatterns = patterns('blog.views',
    url(r'^$', 'blog_main'),
    url(r'^/new-post$', 'new_post'),
    url(r'^/([-a-zA-Z0-9]+)/$', 'view_post'),
)
