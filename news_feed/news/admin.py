from django.contrib import admin
from .models import Feed, LikeDislike

class FeedAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_at', 'view_count', 'likes', 'dislikes')
    search_fields = ('title',)
    list_filter = ('published_at',)
    readonly_fields = ('view_count', 'likes', 'dislikes')
    fields = ('title', 'body', 'image', 'youtube_video_url', 'view_count', 'likes', 'dislikes')

admin.site.register(Feed, FeedAdmin)
admin.site.register(LikeDislike)