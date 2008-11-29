from django.db import models


class StaticPage(models.Model):
    title = models.CharField(max_length=48)
    slug = models.SlugField(max_length=24)
    text = models.TextField()

    def __unicode__(self):
        return self.title
