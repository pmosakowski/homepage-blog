from django.conf.urls import patterns, include, url
from .views import ContactFormView

urlpatterns = patterns('contactform.views',
    url(r'^/?$', ContactFormView.as_view()),
)
