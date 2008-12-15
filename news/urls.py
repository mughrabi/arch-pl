from django.conf.urls.defaults import patterns
from feeds import LatestNews

feeds = { 'rss': LatestNews, }

urlpatterns = patterns("",
        (r'^/(?P<url>.*)/$',   'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
)

urlpatterns += patterns("news.views",
        (r"^/$",                            "latest"),
        (r"^/older/(?P<offset>\d+)/$",      "latest"),
        (r"^/create/$",                     "create"),
        (r"^/showall/$",                    "show_all"),
        (r"^/(?P<slug>[\w-]+)/$",           "details"),
        (r"^/(?P<slug>[\w-]+)/show/$",      "details"),
        (r"^/(?P<slug>[\w-]+)/edit/$",      "edit"),
        (r"^/(?P<slug>[\w-]+)/delete/$",    "delete"),
        (r"^/(?P<slug>[\w-]+)/confirm/$",   "confirm"),
)
