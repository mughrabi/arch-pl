from models import News
from django.contrib import admin

class NewsAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}



admin.site.register(News, NewsAdmin)
