from django.contrib import admin
from .models import Shelf, Audio, Video, Image

class AudioInline(admin.TabularInline):
    model = Audio
    extra = 0

class ImageInline(admin.TabularInline):
    model = Image
    extra = 0

class VideoInline(admin.TabularInline):
    model = Video
    extra = 0

class ShelfAdmin(admin.ModelAdmin):
    list_display =('pk', 'name', 'state', 'library_user', 'modified', 'created')
    date_hierarchy = 'created'
    list_filter  = ('state',)
    search_fields = ('name', )
    link_fields = ('pk', 'name')
    inlines = [
        AudioInline, ImageInline, VideoInline
    ]

    def library_user(self, obj):
        return obj.library.user
    library_user.allow_tags = False
    library_user.short_description = 'Library for'

admin.site.register(Shelf, ShelfAdmin)
