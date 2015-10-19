from django.conf.urls import patterns, url
from django.contrib import admin
from fortytwo_test_task import settings
from django.conf.urls.static import static

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', 'apps.hello.views.home', name='home'),
    url(r'^requests/', 'apps.hello.views.req', name='req'),
    url(r'^edit/', 'apps.hello.views.edit', name='edit'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'registration/login.html'},
                              name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
