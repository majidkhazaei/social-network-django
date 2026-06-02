from django.contrib import admin

from home.models import Post, Comment

@admin.register(Post)

class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'slug', 'created')
    list_filter = ('slug',)
    search_fields = ('user',)
    prepopulated_fields = {'slug': ('body',)}
    raw_id_fields = ('user',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'is_reply', 'created')
    raw_id_fields = ('user','post','reply')