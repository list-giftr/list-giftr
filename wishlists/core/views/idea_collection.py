from typing import Any

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from core import models
from core.mixins import OwnedObjectMixin


class IdeaCollectionCreateView(LoginRequiredMixin, CreateView):
    model = models.IdeaCollection
    fields = ["name"]
    template_name_suffix = "_create"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        obj = form.save(commit=False)
        obj.owner = self.request.user

        return super().form_valid(form)


class IdeaCollectionDeleteView(OwnedObjectMixin, DeleteView):
    context_object_name = "idea_collection"
    model = models.IdeaCollection
    success_url = reverse_lazy("idea-collection-list")

    def form_valid(self, *args, **kwargs):
        # Call the parent method first to ensure the deletion succeeds before we
        # add the success message.
        response = super().form_valid(*args, **kwargs)

        messages.add_message(
            self.request,
            messages.SUCCESS,
            _("Deleted idea collection '%(collection_name)s'.")
            % {"collection_name": self.object.name},
        )

        return response

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["idea_count"] = self.object.ideas.count()

        return context


class IdeaCollectionListView(OwnedObjectMixin, ListView):
    context_object_name = "idea_collections"
    model = models.IdeaCollection
    template_name = "core/ideacollection_list.html"

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().annotate(idea_count=Count("idea"))


class IdeaCollectionUpdateView(OwnedObjectMixin, UpdateView):
    context_object_name = "idea_collection"
    model = models.IdeaCollection
    fields = ["name"]
    template_name_suffix = "_update_form"


class IdeaCollectionDetailView(OwnedObjectMixin, DetailView):
    context_object_name = "idea_collection"
    model = models.IdeaCollection
    template_name = "core/ideacollection_detail.html"
