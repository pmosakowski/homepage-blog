from django.conf.urls import patterns, include, url
from .views import CategoryDetailView, CategoryListView

urlpatterns = patterns('blog.views',
    url(r'^$', 'blog_main'),
    url(r'^/new-post$', 'new_post'),
    url(r'^/categories/?$', CategoryListView.as_view()),
    url(r'^/category/(?P<slug>[-\w]+)/?$', CategoryDetailView.as_view()),
    url(r'^/post/([-a-zA-Z0-9]+)/$', 'view_post'),
)
