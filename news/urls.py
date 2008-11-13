from django.conf.urls.defaults import patterns

urlpatterns = patterns("news.views",
        (r"^/$",                        "latest"),
        (r"^/create/$",                 "add_news"),
        (r"^/show/(?P<slug>[\w-]+)/$",   "details"),
)
