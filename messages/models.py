from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

class MessageBox(models.Model):
    receiver = models.ForeignKey(User, related_name='receiver')
    sender = models.ForeignKey(User, related_name='sender')
    text = models.TextField(_('message'))
    date = models.DateTimeField(_('date'), auto_now_add=True)
    is_new = models.BooleanField(default=False)

    def __unicode__(self):
        return u"Message at %s to %s" % (self.date, self.receiver)

    def get_absolute_url(self):
        return u"/messages/%d/" % self.id

    def new_messages(self, user):
        return MessageBox.object.filter(is_new=True, receiver=user)

    class Meta:
        ordering = ("-date", )
