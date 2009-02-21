from django.conf.urls.defaults import patterns

urlpatterns = patterns("messages.views",
        (r"^/$",                       "show_user_messages_box"),
        (r"^list/$",                   "show_user_messages_box"),
        (r"^write/$",                  "write_user_message"),
        (r"^(?P<id>\d+)/delete/$",     "delete_user_message"),
        (r"^(?P<id>\d+)/response/$",   "response_user_message"),
)
