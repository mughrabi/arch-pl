from django.conf.urls.defaults import patterns

urlpatterns = patterns("messages.views",
        (r"^sended/$",                 "sended_user_messages"),
        (r"^received/$",               "received_user_messages"),
        (r"^write/$",                  "write_user_message"),
        (r"^(?P<id>\d+)/delete/$",     "delete_user_message"),
        (r"^(?P<id>\d+)/response/$",   "response_user_message"),
)
