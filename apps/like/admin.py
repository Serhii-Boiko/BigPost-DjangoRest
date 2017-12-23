from django.conf import settings
from django.contrib import admin

from apps.like.models import Like


class LikeAdmin(admin.ModelAdmin):
    """ Admin interface for Like model """
    list_display = ['author', 'date_created', 'cancelled']
    list_display_links = ['author']
    list_per_page = settings.ADMIN_LIST_PER_PAGE
    readonly_fields = ['date_created']


admin.site.register(Like, LikeAdmin)
