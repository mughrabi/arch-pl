from django.contrib.syndication.feeds import Feed
from models import Thread

class LatestThreads(Feed):
    title = "Forum Arch Linux"
    link = "/forum/"
    description = "Ostatnio aktywne tematy polskiego forum Arch Linuksa"

    def items(self):
        return Thread.objects.order_by('latest_post_date')[:10]
