from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet


class OwnedObjectMixin(LoginRequiredMixin):
    object_owner_field = "owner"

    def get_queryset(self) -> QuerySet[Any]:
        filter = {self.object_owner_field: self.request.user}

        return super().get_queryset().filter(**filter)
