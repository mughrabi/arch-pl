from django.conf.urls.defaults import patterns
from feeds import LatestThreads, ThreadFeed

urlpatterns = patterns("forum.views",
        (r"^$",                                "thread_list"),
        (r"^get_markdown/$",                   "text_to_markdown"),
        (r"^older/(?P<offset_step>\d+)/$",     "thread_list"),
        (r"^new_thread/$",                     "add_thread"),
        (r"^search/$",                         "quick_search"),
        (r"^search/(?P<searchtext>.+)/$",      "quick_search"),
        (r"^advanced_search/$",                "advanced_search"),
        (r"^all_readed/$",                     "mark_all_read"),
        (r"^my_activity/$",                    "user_latest_active_threads"),

        (r"^thread/(?P<thread_slug>[\w-]+)/$",                                     "thread"),
        (r"^thread/(?P<thread_slug>[\w-]+)/offset/(?P<offset_step>\d+)/$",         "thread"),
        (r"^thread/(?P<thread_slug>[\w-]+)/reply/$",                               "add_post"),
        (r"^thread/(?P<thread_slug>[\w-]+)/reply/quote/(?P<post_id>\d+)/$",        "add_post"),
        (r"^thread/(?P<thread_slug>[\w-]+)/(?P<post_id>\d+)/edit/$",               "edit_post"),
        (r"^thread/(?P<thread_slug>[\w-]+)/(?P<post_id>\d+)/delete/$",             "delete_post"),
        (r"^thread/(?P<thread_slug>[\w-]+)/delete/$",                              "delete_thread"),
        (r"^thread/(?P<thread_slug>[\w-]+)/latest_seen_post/$",                    "latest_seen_post"),
        (r"^thread/(?P<thread_slug>[\w-]+)/toggle_block/$",                        "block_thread"),
        (r"^thread/(?P<thread_slug>[\w-]+)/toggle_solved/$",                       "toggle_solved"),
        (r"^thread/(?P<thread_slug>[\w-]+)/toggle_sticky/$",                       "toggle_sticky"),
)

feeds = { 'latest': LatestThreads, }

urlpatterns += patterns("",
        (r"^thread/(?:[\w-]+)/(?P<url>.*)/$", 'django.contrib.syndication.views.feed', {'feed_dict': {'feed': ThreadFeed}}),
        (r'^feeds/(?P<url>.*)/$',        'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
)
