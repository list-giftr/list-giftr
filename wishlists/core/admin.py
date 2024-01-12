from typing import Any
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


@admin.register(models.GiftIdea)
class GiftIdeaAdmin(admin.ModelAdmin):
    fields = ("id", "collection", "description", "link", "created_at", "updated_at")
    list_display = ("description", "collection", "created_at", "updated_at")
    readonly_fields = ("id", "created_at", "updated_at")

    def get_form(
        self, request: Any, obj: Any | None = ..., change: bool = ..., **kwargs: Any
    ) -> Any:
        form = super().get_form(request, obj, change, **kwargs)

        form.base_fields["link"].required = False

        return form
