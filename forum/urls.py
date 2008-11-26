from django.conf.urls.defaults import patterns

urlpatterns = patterns("forum.views",
        (r"^/$",                                                                "category_list"),
        (r"^/search/$",                                                         "quick_search"),
        (r"^/search/(?P<searchtext>.+)/$",                                      "quick_search"),
        (r"^/all_readed/$",                                                     "mark_all_read"),
        (r"^/show_unreaded/$",                                                  "show_unreaded"),
        (r"^/thread/(?P<thread_slug>[\w-]+)/$",                                 "thread"),
        (r"^/thread/(?P<thread_slug>[\w-]+)/offset/(?P<offset_step>\d+)/$",     "thread"),
        (r"^/thread/(?P<thread_slug>[\w-]+)/solved/$",                          "toggle_solved"),
        (r"^/(?P<category_slug>[\w-]+)/$",                                      "thread_list"),
        (r"^/(?P<category_slug>[\w-]+)/offset/(?P<offset_step>\d+)/$",          "thread_list"),
        (r"^/(?P<category_slug>[\w-]+)/new/$",                                  "add_thread"),

        (r"^/thread/(?P<thread_slug>[\w-]+)/reply/$",                               "add_post"),
        (r"^/thread/(?P<thread_slug>[\w-]+)/reply/quote/(?P<post_id>\d+)/$",  "add_post"),
        (r"^/thread/(?P<thread_slug>[\w-]+)/(?P<post_id>\d+)/edit/$",               "edit_post"),
        (r"^/thread/(?P<thread_slug>[\w-]+)/(?P<post_id>\d+)/delete/$",             "delete_post"),
)
