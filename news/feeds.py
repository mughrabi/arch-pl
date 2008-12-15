# -*- coding: utf-8 -*-
from django.contrib.syndication.feeds import Feed
from models import News

class LatestNews(Feed):
    title = "Nowości Arch Linux"
    link = "/"
    description = "Wiadomości ze świata Arch Linuksa"

    def items(self):
        return News.objects.exclude(show=False)[:10]
