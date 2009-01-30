# -*- coding: utf-8 -*-
from django.contrib.syndication.feeds import Feed
from models import News

class LatestNews(Feed):
    title = "Nowości Arch Linux"
    link = "/"
    description = "Wiadomości ze świata Arch Linuksa"

    def items(self):
        return News.objects.exclude(show=False)[:10]

class AllNews(Feed):
    title = "Nowości Arch Linux"
    link = "/"
    description = "Wiadomości ze świata Arch Linuksa"

    def items(self):
        return News.objects.all()[:10]

class UnpublishedNews(Feed):
    title = "Arch Linux news - propozycje"
    link = "/"
    description = "Niepotwierdzone wiadomości ze świata Arch Linuksa"

    def items(self):
        return News.objects.exclude(show=True)[:10]
