from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.views.generic.list import ListView

from core import models


class IdeaListsView(LoginRequiredMixin, ListView):
    context_object_name = "idea_lists"
    model = models.IdeaList
    template_name = "core/idealist_list.html"

    def get_queryset(self) -> QuerySet[Any]:
        idea_lists = super().get_queryset()

        return idea_lists.filter(owner=self.request.user)
