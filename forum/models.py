# -*- coding: utf-8 -*-

import datetime
from itertools import chain

from django import forms
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape


class TagSelectWidget(forms.SelectMultiple):
    def __init__(self, *args, **kwds):
        super(TagSelectWidget, self).__init__(*args, **kwds)

    def render(self, name, value, attrs=None, choices=()):
        if value is None: 
            value = []
        has_id = attrs and 'id' in attrs
        final_attrs = self.build_attrs(attrs, name=name)
        output = []
        str_values = set([force_unicode(v) for v in value])
        for i, (option_value, option_label) in enumerate(chain(self.choices, choices)):
            if has_id:
                final_attrs = dict(final_attrs, id='%s_%s' % (attrs['id'], i))
                label_for = u' for="%s"' % final_attrs['id']
            else:
                label_for = ''
            cb = forms.CheckboxInput(final_attrs, 
                    check_test=lambda value: value in str_values)
            option_value = force_unicode(option_value)
            rendered_cb = cb.render(name, option_value)
            option_label = conditional_escape(force_unicode(option_label))
            output.append(u'<label%s>%s %s</label>' % (label_for, rendered_cb, option_label))
        return mark_safe(u'\n'.join(output))


class TagSelectField(forms.MultipleChoiceField):
    widget = TagSelectWidget
    
    def __init__(self, *args, **kwds):
        choices = kwds.pop('choices_generator', 0).choices()
        kwds.update({'choices': choices})
        super(TagSelectField, self).__init__(*args, **kwds)

    def clean(self, value):
        return value


class TagField(models.CharField):
    __metaclass__ = models.SubfieldBase

    def get_internal_type(self):
        return "CharField"

    def __init__(self, choices_generator, separator="|", *args, **kwds):
        self.choices_generator = choices_generator
        self.separator = separator
        super(TagField, self).__init__(*args, **kwds)

    def to_python(self, value):
        if isinstance(value, list):
            return value
        if not value:
            return ""
        return value.split(self.separator)

    def get_db_prep_value(self, value):
        # TODO - separator validation
        return self.separator.join(value)

    def formfield(self, **kwds):
        defaults = {'choices_generator': self.choices_generator}
        defaults.update(kwds)
        return TagSelectField(**defaults)


class ThreadTag(models.Model):
    name = models.CharField(max_length=64, unique=True, blank=False)

    @classmethod
    def choices(cls):
        return [(t.name, t.name) for t in cls.objects.all()]

    def __unicode__(self):
        return u"Tag: %s" % self.name


class Thread(models.Model):
    author = models.ForeignKey(User)
    title = models.CharField(max_length=128)
    slug = models.SlugField(unique=True, max_length=128)
    # special flags
    closed = models.BooleanField(default=False)
    sticky = models.BooleanField(default=False)
    solved = models.BooleanField(default=False)
    # tags
    tags = TagField(ThreadTag, max_length=128)
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
