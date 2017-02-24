from django.contrib import admin

from .models import Post


class PostModel(admin.ModelAdmin):
    list_display = ["title", "timestamp"]
    list_display_links = ["timestamp"]
    list_editable = ["title"]
    list_filter = ["timestamp", "user"]
    search_fields = ["title", "content"]

    class Meta:
        model = Post


admin.site.register(Post, PostModel)