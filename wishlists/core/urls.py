from django.urls import path
from django.views.generic.base import TemplateView

from core.views import gift_idea, idea_collection, robots

urlpatterns = [
    path("", TemplateView.as_view(template_name="core/home.html"), name="index"),
    path(
        "gift-idea/<uuid:pk>",
        gift_idea.GiftIdeaDetailView.as_view(),
        name="gift-idea-detail",
    ),
    path(
        "gift-idea/<uuid:pk>/delete",
        gift_idea.GiftIdeaDeleteView.as_view(),
        name="gift-idea-delete",
    ),
    path(
        "gift-idea/<uuid:pk>/edit",
        gift_idea.GiftIdeaUpdateView.as_view(),
        name="gift-idea-update",
    ),
    path(
        "gift-idea/<uuid:pk>/mentioned",
        gift_idea.gift_idea_mentioned,
        name="gift-idea-mention",
    ),
    path(
        "ideas/",
        idea_collection.IdeaCollectionListView.as_view(),
        name="idea-collection-list",
    ),
    path(
        "ideas/new",
        idea_collection.IdeaCollectionCreateView.as_view(),
        name="idea-collection-create",
    ),
    path(
        "ideas/<uuid:pk>/",
        idea_collection.IdeaCollectionDetailView.as_view(),
        name="idea-collection-detail",
    ),
    path(
        "ideas/<uuid:pk>/delete",
        idea_collection.IdeaCollectionDeleteView.as_view(),
        name="idea-collection-delete",
    ),
    path(
        "ideas/<uuid:pk>/edit",
        idea_collection.IdeaCollectionUpdateView.as_view(),
        name="idea-collection-update",
    ),
    path(
        "ideas/<uuid:pk>/new-idea",
        gift_idea.GiftIdeaCreateView.as_view(),
        name="gift-idea-create",
    ),
    path("robots.txt", robots.robots_txt, name="robots.txt"),
]
