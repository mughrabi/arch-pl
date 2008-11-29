from django.conf.urls.defaults import patterns

urlpatterns = patterns("userprofile.views",
        (r"^/$",                      "user_login"),
        (r"^login/$",                      "user_login"),
        (r"^logout/$",                     "user_logout"),
        (r"^register/$",                   "register"),
        (r"^preferences/$"                 "preferences"),
        (r"^(?P<username>[\w-]+)/$",       "userinfo"),
)
