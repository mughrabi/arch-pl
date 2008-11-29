# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from django.contrib import admin
from settings import DEBUG

admin.autodiscover()

urlpatterns = patterns('',
    (r'^$',                 'news.views.latest'),
    (r'^news',              include('news.urls')),
    (r'^forum',             include('forum.urls')),
    (r'^account',           include('userprofile.urls')),
    (r'^admin/(.*)',        admin.site.root),
)

if DEBUG:
    urlpatterns += patterns('',
    (r'^static/(?P<path>.*)$',
        'django.views.static.serve', {'document_root': 'media_root'}),
    )
