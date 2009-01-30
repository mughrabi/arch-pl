from django.conf.urls.defaults import patterns
from feeds import LatestThreads

urlpatterns = patterns("forum.views",
        (r"^$",                                "thread_list"),
        (r"^older/(?P<offset_step>\d+)/$",     "thread_list"),
        (r"^new_thread/$",                     "add_thread"),
        (r"^search/$",                         "quick_search"),
        (r"^search/(?P<searchtext>.+)/$",      "quick_search"),
        (r"^advanced_search/$",                "advanced_search"),
        (r"^all_readed/$",                     "mark_all_read"),
        (r"^show_unreaded/$",                  "show_unreaded"),
        (r"^my_activity/$",                    "user_latest_active_threads"),

        (r"^thread/(?P<thread_slug>[\w-]+)/$",                                     "thread"),
        (r"^thread/(?P<thread_slug>[\w-]+)/offset/(?P<offset_step>\d+)/$",         "thread"),
        (r"^thread/(?P<thread_slug>[\w-]+)/solved/$",                              "toggle_solved"),
        (r"^thread/(?P<thread_slug>[\w-]+)/reply/$",                               "add_post"),
        (r"^thread/(?P<thread_slug>[\w-]+)/reply/quote/(?P<post_id>\d+)/$",        "add_post"),
        (r"^thread/(?P<thread_slug>[\w-]+)/(?P<post_id>\d+)/edit/$",               "edit_post"),
        (r"^thread/(?P<thread_slug>[\w-]+)/(?P<post_id>\d+)/delete/$",             "delete_post"),
        (r"^thread/(?P<thread_slug>[\w-]+)/delete/$",                              "delete_thread"),
        (r"^thread/(?P<thread_slug>[\w-]+)/block/$",                               "block_thread"),
        (r"^thread/(?P<thread_slug>[\w-]+)/latest_seen/$",                         "latest_seen_post"),
)

feeds = { 'latest': LatestThreads, }

urlpatterns += patterns("",
        (r'^/feeds/(?P<url>.*)/$',   'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
)
