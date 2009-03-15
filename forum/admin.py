# -*- coding: utf-8 -*-

from models import Thread, Post, ThreadTag
from django.contrib import admin
#from django.utils.translation import ugettext_lazy as _

class ThreadAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Post)
admin.site.register(Thread, ThreadAdmin)
admin.site.register(ThreadTag)

