from django.contrib import admin

from .models import *


# admin 1111
@admin.register(Links)
class LinksAdmin(admin.ModelAdmin):
    list_display = ('name', 'link', 'status')


@admin.register(Articles)
class ArticlesAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'photo', 'published', 'description')
