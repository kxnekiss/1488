from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, Room, Booking


class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('failed_attempts', 'first_login')}),
    )


admin.site.register(User, UserAdmin)
admin.site.register(Room)
admin.site.register(Booking)
