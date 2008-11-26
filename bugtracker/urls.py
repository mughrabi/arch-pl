from django.conf.urls.defaults import patterns

urlpatterns = patterns("bugtracker.views",
        (r"^/$",                                    "bug_reported"),
        (r"^old/$",                                 "bug_closed"),
        (r"^/report/$",                             "bug_report"),
        (r"^/show/(?P<bug_id>\d+)/$",               "bug_show"),
        (r"^/show/(?P<bug_id>\d+)/comment/$",       "bug_comment"),
)
