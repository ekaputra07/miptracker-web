from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

from tracker.views import HomePage, plain_page

urlpatterns = patterns('',
    url(r'^$', HomePage.as_view(), name='homepage'),
    url(r'^plain/$', plain_page, name='plain_page'),
)
