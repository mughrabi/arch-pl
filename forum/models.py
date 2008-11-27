# -*- coding: utf-8 -*-


from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Thread(models.Model):
    author = models.ForeignKey(User)
    title = models.CharField(max_length=128)
    slug = models.SlugField(unique=True, max_length=128)
    keywords = models.CharField(max_length=64,
            help_text="Split keywords with signgle space")
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
        t.post_count = t.post_set.count() - 1
        t.save()

    def delete(self):
        try:
            latest_post_date = Post.objects.exclude(
                    pk=self.id).latest("date").date
        except Post.DoesNotExist:
            latest_post_date = None
        t = self.thread
        # if this one is last, delete thread
        t.post_count = t.post_set.exclude(pk=self.id).count()
        t.latest_post_date = latest_post_date
        t.save()
        if not t.post_count:
            t.delete()
        super(Post, self).delete()


class VisitedThread(models.Model):
    user = models.ForeignKey(User)
    thread = models.ForeignKey(Thread)
    date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s @ %s" % (self.user, self.thread)


class AllVisited(models.Model):
    user = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s # %s" % (self.user, self.date)
