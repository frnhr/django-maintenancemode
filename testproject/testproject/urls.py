from django.conf.urls import patterns, url, include
from django.contrib.admin import site as admin_site

urlpatterns = patterns('',
    url(r'^$', 'testapp.views.index'),
    url(r'^ignored/$', 'testapp.views.ignored'),
    url(r'^admin/', include(admin_site.get_urls(), "admin")),
)
