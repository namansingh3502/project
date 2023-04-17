from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *

# Admin page settings

admin.site.site_header = 'TOTP Admin'
admin.site.index_title = 'Features area'
admin.site.site_title = 'HTML title from Administration'


@admin.register(UserProfile)
class UserProfileAdmin(UserAdmin):
    list_display = ('username', 'is_active', 'is_staff', 'is_superuser')

    list_filter = ('groups', 'is_staff', 'is_superuser')

    fieldsets = (
        ('Profile', {
            'fields': (
                'username',
                'first_name',
                'last_name',
                'email',
                'phone',
            )
        }),
        ('Permissions', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                # 'groups',
                # 'user_permissions'
            )
        }),
        ('Important dates', {
            'fields': (
                'last_login',
                'date_joined'
            )
        }),
    )

    add_fieldsets = (
        ('Authentication Details', {
            'fields': (
                'username',
                'password1',
                'password2'
            )
        }),
        ('Profile', {
            'fields': (
                'first_name',
                'middle_name',
                'last_name',
                'gender',
                'department',
                'email',
                'phone',

            )
        }),
        ('Permissions', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                # 'groups',
                # 'user_permissions'
            )
        }),
    )


@admin.register(UserTOTPDetails)
class UserTOTPDetails(admin.ModelAdmin):
    list_display = ("user", "platform")

    list_filter = ("platform",)

    fieldsets = (
        ("Totp Details", {
            'fields': (
                "user",
                "platform",
                "key",
                "delay"
            )
        }),
    )
