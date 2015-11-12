from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from fortytwo_test_task import settings

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^', include('apps.hello.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$',
        'django.contrib.auth.views.login',
        {'template_name': 'registration/login.html'},
        name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
        {'next_page': '/'}, name='logout'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
