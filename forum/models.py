# -*- coding: utf-8 -*-

import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Category(models.Model):
    slug = models.SlugField(_("Slug field"), max_length=24)
    name = models.CharField(_("Name"), max_length=24)
    description = models.TextField(_("Description"))
    thread_count = models.PositiveIntegerField(_("Topics"), default=0)
    post_count = models.PositiveIntegerField(_("Posts"), default=0)
    latest_thread_date = models.DateTimeField(auto_now=True)
    latest_thread_author = models.ForeignKey(User, default=1)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "/forum/%s/" % self.slug


class Thread(models.Model):
    author = models.ForeignKey(User)
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, max_length=122)
    category = models.ForeignKey(Category)
    # special flags
    closed = models.BooleanField(default=False)
    sticky = models.BooleanField(default=False)
    solved = models.BooleanField(default=False)
    # thread info
    post_count = models.PositiveIntegerField(_("Posts"), default=0)
    view_count = models.PositiveIntegerField(_("Views"), default=0)
    # info about last post
    latest_post_date = models.DateTimeField(
            _("Latest Post Time"), auto_now=True)

    class Meta:
        ordering = ("-sticky", "latest_post_date")

    def get_absolute_url(self):
        return "/forum/thread/%s/" % self.slug

    def __unicode__(self):
        return self.title + " by " + self.author.username

    def _get_latest_post(self):
        "Return latest related post or None"
        if not hasattr(self, "__latest_post"):
            try:
                self.__latest_post = Post.objects.filter(
                        thread__pk=self.id).latest("date")
            except Post.DoesNotExist:
                self.__latest_post = None
        return self.__latest_post
    latest_post = property(_get_latest_post)

    def save(self, force_insert=False, force_update=False):
        c = self.category
        c.post_count = c.thread_set.count()
        c.latest_thread_date = datetime.datetime.now()
        c.latest_thread_author = self.author
        super(Thread, self).save(force_insert, force_update)

    def delete(self):
        super(Thread, self).delete()
        c = self.category
        c.threads = c.thread_set.count()
        c.posts = Post.objects.filter(
                thread__category__pk=c.id).count()
        latest_post = Post.objects.latest("date")
        c.latest_thread_date = latest_post.date
        c.latest_thread_author = latest_post.author
        c.save()


class Post(models.Model):
    thread = models.ForeignKey(Thread)
    author = models.ForeignKey(User)
    text = models.TextField()
    date = models.DateTimeField(_("Last modification"), auto_now=True)

    class Meta:
        ordering = ("date", )

    def __unicode__(self):
        return "post by " + self.author.username

    def save(self, force_insert=False, force_update=False):
        new_post = False
        super(Post, self).save(force_insert, force_update)
        t = self.thread
        t.latest_post_time = t.post_set.latest("date").date
        t.posts = t.post_set.count()
        t.save()
        c = self.thread.category
        c.thread_count = c.thread_set.count()
        c.post_count = Post.objects.filter(
                thread__category__pk=c.id).count()
        c.latest_thread_date = datetime.datetime.now()
        c.latest_thread_author = t.author
        c.save()

    def delete(self, *args, **kwds):
        try:
            latest_post_date = Post.objects.exclude(
                    pk=self.id).latest("date").date
        except Post.DoesNotExist:
            latest_post_date = None
        t = self.thread
        c = self.thread.category
        c.post_count = Post.objects.filter(
                thread__category__pk=c.id).exclude(pk=self.id).count()
        c.save()
        # if this one is last, delete thread
        if not self.id == t.latest_post.id:
            t.post_count = t.post_set.exclude(pk=self.id).count()
            t.latest_post_date = latest_post_date
            t.save()
        else:
            t.delete()
        super(Post, self).delete()


class VisitedThread(models.Model):
    user = models.ForeignKey(User)
    thread = models.ForeignKey(Thread)
    date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s @ %s" % (self.user, self.thread)


class AllCategoryVisit(models.Model):
    user = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s # %s" % (self.user, self.date)
