from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'testapp.views.index'),
    url(r'^ignored/$', 'testapp.views.index'),
)
