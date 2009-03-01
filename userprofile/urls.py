from django.conf.urls.defaults import patterns

urlpatterns = patterns("userprofile.views",
        (r"^login/$",                      "user_login"),
        (r"^logout/$",                     "user_logout"),
        (r"^register/$",                   "register"),
        (r"^preferences/$",                "user_preferences"),
        (r"^latest_login_date/$",          "latest_login_date"),
)
