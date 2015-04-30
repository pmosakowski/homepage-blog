from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'mainpage.views.main_page', name='home'),
    url(r'^about$', 'mainpage.views.about_page', name='about'),
    url(r'^login$', 'mainpage.views.login_page', name='login'),
    url(r'^logout$','mainpage.views.logout_page', name='logout'),

    url(r'^blog', include('blog.urls')),
    # url(r'^homepage/', include('homepage.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
