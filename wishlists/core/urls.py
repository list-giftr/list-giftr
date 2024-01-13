from django.urls import path

from core.views import gift_idea, idea_collection

urlpatterns = [
    path(
        "gift-idea/<uuid:pk>",
        gift_idea.GiftIdeaDetailView.as_view(),
        name="gift-idea-detail",
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
]
