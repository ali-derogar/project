from atexit import register
from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin

UserAdmin.fieldsets[2][1]['fields'] = (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                    'is_author',
                    'special_user'
                )
UserAdmin.list_display += ("is_special_user", "is_author")


admin.site.register(User,UserAdmin)