from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class News(models.Model):
    slug = models.SlugField(max_length=24)
    author = models.ForeignKey(User)
    title = models.CharField(max_length=64)
    date = models.DateTimeField(auto_now=True)
    text = models.TextField()
    show = models.BooleanField(_("Show on main page"), default=False)

    class Meta:
        ordering = ("-date", )

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "/news/%s/" % self.slug

    def save(self, force_insert=False, force_update=False):
        super(News, self).save(force_insert, force_update)


