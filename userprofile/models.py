import urllib
import hashlib

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True, null=False)
    jabber = models.EmailField(blank=True)
    jabber_notify = models.BooleanField(
            _('Jabber notifycation'), default=False)
    signature = models.CharField(max_length=256, blank=True)
    about = models.TextField()

    def avatar(self):
        if not hasattr(self, "__avatar"):
            self.__avatar = \
                "http://www.gravatar.com/avatar.php?" + urllib.urlencode({
                    'gravatar_id': hashlib.md5(self.user.email).hexdigest(),
                    'default': "/static/images/default_avatar.png",
                    'size': "70",
                })
        return self.__avatar

    def __unicode__(self):
        return "%s profile" % self.user

