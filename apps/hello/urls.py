from django.conf.urls import patterns, url
from django.contrib import admin
from apps.hello.views import HomeView

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^requests/', 'apps.hello.views.req', name='req'),
)
