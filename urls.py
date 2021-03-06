# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include
from django.contrib import admin
from settings import DEBUG

admin.autodiscover()

urlpatterns = patterns('',
    (r'^$',                                 'news.views.latest'),
    (r'^users/(?P<username>[\w-]+)/$',      'userprofile.views.userinfo'),

    (r'^news/',                             include('news.urls')),
    (r'^forum/',                            include('forum.urls')),
    (r'^accounts/',                         include('userprofile.urls')),

    (r'^admin/(.*)',                        admin.site.root),

    (r'^',                                  include('staticpages.urls')),
)

if DEBUG:
    urlpatterns += patterns('',
    (r'^static/(?P<path>.*)$',
        'django.views.static.serve', {'document_root': 'media_root'}),
    )
