# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from django.contrib import admin
from settings import DEBUG

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/(.*)',        admin.site.root),
    (r'^uzytkownicy/',      include('registration.urls')),
    (r'^forum',             include('forum.urls')),
)

if DEBUG:
    urlpatterns += patterns('',
    (r'^static/(?P<path>.*)$',
        'django.views.static.serve', {'document_root': 'media_root'}),
    )
