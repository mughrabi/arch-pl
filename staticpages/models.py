from django.db import models


class StaticPage(models.Model):
    title = models.CharField(max_length=64)
    slug = models.SlugField(max_length=24)
    text = models.TextField()
    update = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title
