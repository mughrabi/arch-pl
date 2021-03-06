from django.contrib.syndication.feeds import Feed
from models import Thread

class LatestThreads(Feed):
    title = "Forum Arch Linux"
    link = "/forum/"
    description = "Ostatnio aktywne tematy polskiego forum Arch Linuksa"

    def items(self):
        return Thread.objects.order_by('latest_post_date')[:10]

class ThreadFeed(Feed):
    def get_object(self, bits):
        # In case of "/rss/beats/0613/foo/bar/baz/", or other such clutter,
        # check that bits has only one member.
        print "bits >>> ", bits
        if len(bits) != 1:
            raise Thread.DoesNotExist
        return Thread.objects.get(slug=bits[0])

    def title(self, obj):
        if not obj:
            raise feeds.FeedDoesNotExist
        return "Arch Linux forum : %s" % obj.title

    def link(self, obj):
        if not obj:
            raise FeedDoesNotExist
        return obj.get_absolute_url()

    def description(self, obj):
        return "%s : %s" % (obj.title, "opis")

    def items(self):
        return Thread.objecs.post_set.all()
