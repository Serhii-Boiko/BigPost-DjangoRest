from django.conf import settings
from django.contrib import admin

from apps.post.models import Post


class PostAdmin(admin.ModelAdmin):
    """ Admin interface for Post model """
    list_display = ['title', 'author', 'date_created']
    list_display_links = ['title']
    list_per_page = settings.ADMIN_LIST_PER_PAGE
    readonly_fields = ['date_created', 'uuid']


admin.site.register(Post, PostAdmin)
