from django.conf.urls import patterns, include, url
from .views import ContactFormView, ThanksView

urlpatterns = patterns('contactform.views',
    url(r'^/?$', ContactFormView.as_view()),
    url(r'^/thanks/?$', ThanksView.as_view()),
)
