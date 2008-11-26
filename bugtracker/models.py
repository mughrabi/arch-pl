from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

import datetime

class Bug(models.Model):
    title = models.CharField(_("Bug name"), max_length=128)
    description = models.TextField(_("Description"))
    date_reported = models.DateTimeField(auto_now_add=True)
    reported_by = models.ForeignKey(User)
    closed = models.BooleanField(default=False)
    closed_date = models.DateTimeField()
    closed_by = models.ForeignKey(User, required=False)

    def close(self, user):
        self.closed_by = user
        self.date_close = datetime.datetime.now()
        self.closed = True
        self.save()

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.date_reported)


class BugComment(models.Model):
    bug = models.ForeignKey(Bug)
    author = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

    def __unicode__(self):
        return "%s - %s" % (self.author, self.text[:100])
