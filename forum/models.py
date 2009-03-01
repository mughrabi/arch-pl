# -*- coding: utf-8 -*-

import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Thread(models.Model):
    author = models.ForeignKey(User)
    title = models.CharField("", max_length=128)
    slug = models.SlugField(unique=True, max_length=128)
    # special flags
    closed = models.BooleanField(default=False)
    sticky = models.BooleanField(default=False)
    solved = models.BooleanField(default=False)
    # thread info
    post_count = models.PositiveIntegerField(_("Posts"), default=0)
    view_count = models.PositiveIntegerField(_("Views"), default=0)
    # info about latest post
    latest_post_date = models.DateTimeField(_("Latest Post time"),
            default=datetime.datetime.now())
    latest_post_author = models.ForeignKey(User, related_name="User")

    class Meta:
        ordering = ("-sticky", "-latest_post_date")

    def get_absolute_url(self):
        return "/forum/thread/%s/" % self.slug

    def __unicode__(self):
        return "%s, napisany przez %s" % \
                (self.title, self.author.username)

    @property
    def latest_post(self):
        "Return latest related post or None"
        if not hasattr(self, "__latest_post"):
            try:
                self.__latest_post = Post.objects.filter(
                        thread__pk=self.id).latest("date")
            except Post.DoesNotExist:
                self.__latest_post = None
        return self.__latest_post


class Post(models.Model):
    thread = models.ForeignKey(Thread)
    author = models.ForeignKey(User)
    text = models.TextField("")
    date = models.DateTimeField(_("Last modification"), auto_now=True)

    class Meta:
        ordering = ("date", )

    def __unicode__(self):
        return "post by " + self.author.username

    def save(self, force_insert=False, force_update=False):
        super(Post, self).save(force_insert, force_update)
        t = self.thread
        lp = t.post_set.latest("date")
        t.latest_post_date = lp.date
        t.latest_post_author = lp.author
        t.post_count = t.post_set.count() - 1
        t.save()

    def delete(self):
        t = self.thread
        t.post_count = t.post_set.exclude(pk=self.id).count()
        try:
            lp = t.post_set.exclude(pk=self.id).latest("date")
            t.latest_post_date = lp.date
            t.latest_post_author = lp.author
        except Post.DoesNotExist:
            t.delete()
        else:
            t.save()
        finally:
            super(Post, self).delete()
