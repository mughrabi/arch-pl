from django.conf.urls.defaults import patterns

urlpatterns = patterns("news.views",
        (r"^/$",                            "latest"),
        (r"^/older/(?P<offset>\d+)/$",      "latest"),
        (r"^/create/$",                     "create"),
        (r"^/showall/$",                    "show_all"),
        (r"^/(?P<slug>[\w-]+)/show/$",      "details"),
        (r"^/(?P<slug>[\w-]+)/edit/$",      "edit"),
        (r"^/(?P<slug>[\w-]+)/delete/$",    "delete"),
        (r"^/(?P<slug>[\w-]+)/confirm/$",   "confirm"),
)
