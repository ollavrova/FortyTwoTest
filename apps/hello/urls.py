from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^$', 'apps.hello.views.home', name='home'),
    url(r'^requests/', 'apps.hello.views.req', name='req'),
    url(r'^edit/(?P<pk>\d+)/$', 'apps.hello.views.edit', name='edit'),
)
