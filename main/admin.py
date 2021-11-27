from django.contrib import admin

from main.models import BaseUser


@admin.register(BaseUser)
class BaseUserAdmin(admin.ModelAdmin):
    pass
