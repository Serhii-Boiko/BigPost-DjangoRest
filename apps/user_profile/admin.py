from django.conf import settings
from django.contrib import admin

from apps.user_profile.models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    """ Admin interface for UserProfile model """
    list_display = ['first_name', 'last_name', 'email']
    list_display_links = ['first_name', 'last_name']
    list_per_page = settings.ADMIN_LIST_PER_PAGE
    readonly_fields = ['uuid']


admin.site.register(UserProfile, UserProfileAdmin)
