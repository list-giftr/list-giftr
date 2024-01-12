from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from core import models


class IdeaCollectionListView(LoginRequiredMixin, ListView):
    context_object_name = "idea_collections"
    model = models.IdeaCollection
    template_name = "core/ideacollection_list.html"

    def get_queryset(self) -> QuerySet[models.IdeaCollection]:
        idea_lists = super().get_queryset()

        return idea_lists.filter(owner=self.request.user)


class IdeaCollectionDetailView(LoginRequiredMixin, DetailView):
    context_object_name = "idea_collection"
    model = models.IdeaCollection
    template_name = "core/ideacollection_detail.html"

    def get_queryset(self) -> QuerySet[models.IdeaCollection]:
        return super().get_queryset().filter(owner=self.request.user)


class GiftIdeaDetailView(LoginRequiredMixin, DetailView):
    context_object_name = "gift_idea"
    model = models.GiftIdea
    template_name = "core/giftidea_detail.html"

    def get_queryset(self) -> QuerySet[models.GiftIdea]:
        return super().get_queryset().filter(collection__owner=self.request.user)
