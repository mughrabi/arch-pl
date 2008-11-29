from django.conf.urls.defaults import patterns

urlpatterns = patterns("staticpages.views",
        (r"^(?P<slug>[\w\-]+)/$",                "show_static_page"),
)
