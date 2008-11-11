# -*- coding: utf-8 -*-

from models import Category, Thread, Post, VisitedThread, AllCategoryVisit
from django.contrib import admin
#from django.utils.translation import ugettext_lazy as _

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

class ThreadAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Post)
admin.site.register(VisitedThread)
admin.site.register(AllCategoryVisit)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Thread, ThreadAdmin)

