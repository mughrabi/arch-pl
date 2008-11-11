import urllib
import hashlib

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True, null=False)
    gravatar = models.EmailField(default='')
    jabber = models.EmailField(blank=True)
    jabber_notify = models.BooleanField(_('Jabber notifycation'), default=False)

    def avatar(self):
        default = "http://www.betternetworker.com/files/imagecache/avatar_profile/avatars/default-avatar-85x85.jpg"
        email = str(self.gravatar) or str(self.user.email)
        if not email:
            return default
        gravatar_url = "http://www.gravatar.com/avatar.php?" + urllib.urlencode({
            'gravatar_id': hashlib.md5(email).hexdigest(),
            'default': default,
            'size': "80",
        })
        return gravatar_url

    def __unicode__(self):
        return "UserProfile of %s" % self.user


