from models import StaticPage
from django.contrib import admin

class StaticPageAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}



admin.site.register(StaticPage, StaticPageAdmin)
