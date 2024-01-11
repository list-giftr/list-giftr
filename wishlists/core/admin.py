from django.contrib import admin

from core import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(models.IdeaList)
class IdeaListAdmin(admin.ModelAdmin):
    fields = ("id", "owner", "name", "created_at", "updated_at")
    list_display = ("name", "owner", "created_at", "updated_at")
    readonly_fields = ("id", "created_at", "updated_at")
