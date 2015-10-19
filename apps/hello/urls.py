from django.conf.urls import patterns, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', 'apps.hello.views.home', name='home'),
    url(r'^requests/', 'apps.hello.views.req', name='req'),
)
