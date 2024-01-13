import uuid
from typing import Any

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from core import forms, models
from core.mixins import OwnedObjectMixin


class GiftIdeaCreateView(LoginRequiredMixin, CreateView):
    model = models.GiftIdea
    form_class = forms.GiftIdeaForm
    template_name_suffix = "_create_form"

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.collection = self._get_collection()

        return super().form_valid(form)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["collection"] = self._get_collection()

        return context

    def _get_collection(self):
        return get_object_or_404(
            models.IdeaCollection,
            pk=self.kwargs["pk"],
            owner=self.request.user,
        )


class GiftIdeaDeleteView(OwnedObjectMixin, DeleteView):
    context_object_name = "idea"
    model = models.GiftIdea
    object_owner_field = "collection__owner"

    def form_valid(self, *args, **kwargs):
        # Call the parent method first to ensure the deletion succeeds before we add the
        # success message.
        response = super().form_valid(*args, **kwargs)

        messages.add_message(
            self.request,
            messages.SUCCESS,
            _("Deleted gift idea '%(idea)s'.") % {"idea": self.object.name},
        )

        return response

    def get_success_url(self) -> str:
        return self.object.collection.get_absolute_url()


class GiftIdeaDetailView(OwnedObjectMixin, DetailView):
    context_object_name = "gift_idea"
    model = models.GiftIdea
    object_owner_field = "collection__owner"
    template_name = "core/giftidea_detail.html"


class GiftIdeaUpdateView(OwnedObjectMixin, UpdateView):
    context_object_name = "gift_idea"
    model = models.GiftIdea
    form_class = forms.GiftIdeaUpdateForm
    object_owner_field = "collection__owner"
    template_name_suffix = "_update_form"


@require_POST
@login_required
def gift_idea_mentioned(request: HttpRequest, pk: uuid.UUID):
    """
    Increment the mention count of the referenced gift idea.

    Once complete, a redirect is returned. If the ``from_list_page``
    GET parameter is present, the redirect is to the detail page of the
    idea's collection. Otherwise it is to the detail page of the idea
    itself.
    """

    gift_idea = get_object_or_404(
        models.GiftIdea, pk=pk, collection__owner=request.user
    )
    gift_idea.increment_mention_count()

    return_to_list_page = "from_list_page" in request.GET
    if return_to_list_page:
        return redirect(gift_idea.collection.get_absolute_url())

    return redirect(gift_idea.get_absolute_url())
