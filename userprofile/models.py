import urllib
import hashlib

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.utils.safestring import SafeUnicode

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True, null=False)
    jabber = models.EmailField(blank=True)
    jabber_notify = models.BooleanField(
            _('Jabber notifycation'), default=False)
    signature = models.TextField(blank=True)

    @property
    def avatar(self):
        if not hasattr(self, "__avatar"):
            self.__avatar = \
                "http://www.gravatar.com/avatar.php?" + urllib.urlencode({
                    'gravatar_id': hashlib.md5(self.user.email).hexdigest(),
                    'size': 80,
                    'default': 'identicon',
                    #'default': "/static/images/default_avatar.png",
                })
        return SafeUnicode(self.__avatar)

    def __unicode__(self):
        return "%s profile" % self.user

