from django.conf import settings
from django.contrib import admin

from apps.comment.models import Comment


class CommentAdmin(admin.ModelAdmin):
    """ Admin interface for Comment model """
    list_display = ['text', 'author', 'date_created']
    list_display_links = ['text']
    list_per_page = settings.ADMIN_LIST_PER_PAGE
    readonly_fields = ['date_created', 'uuid']


admin.site.register(Comment, CommentAdmin)
