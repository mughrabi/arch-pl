import urllib

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True, null=False)
    gravatar = models.CharField(max_length=24)
    jabber = models.EmailField(blank=True)
    jabber_notify = models.BooleanField(_('Jabber notifycation'), default=False)

    def _get_avatar(self):
        if hasattr(self, "__get_avatar"):
            return self.__get_avatar
        default = "http://www.betternetworker.com/files/imagecache/avatar_profile/avatars/default-avatar-85x85.jpg"
        self.__get_avatar = "http://www.gravatar.com/avatar.php?" + urllib.urlencode({
            #'gravatar_id': hashlib.md5(email).hexdigest(),
            'gravatar_id': self.gravatar,
            'default': default,
            'size': "80",
        })
        return self.__get_avatar
    get_avatar = property(_get_avatar)

    def __unicode__(self):
        return "UserProfile of %s" % self.user


