from django.conf.urls.defaults import patterns

urlpatterns = patterns("forum.views",
        (r"^/$",                                        "category_list"),
        (r"^/all_readed/$",                             "mark_all_read"),
        (r"^/thread/(?P<thread_slug>[\w-]+)/$",         "thread"),
        (r"^/thread/(?P<thread_slug>[\w-]+)/reply/$",   "add_post"),
        (r"^/(?P<category_slug>[\w-]+)/$",              "thread_list"),
        (r"^/(?P<category_slug>[\w-]+)/new/$",          "add_thread"),
)
