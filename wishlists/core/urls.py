from django.urls import path

from core import views

urlpatterns = [
    path(
        "gift-idea/<uuid:pk>",
        views.GiftIdeaDetailView.as_view(),
        name="gift-idea-detail",
    ),
    path("ideas/", views.IdeaCollectionListView.as_view(), name="idea-collection-list"),
    path(
        "ideas/new",
        views.IdeaCollectionCreateView.as_view(),
        name="idea-collection-create",
    ),
    path(
        "ideas/<uuid:pk>/",
        views.IdeaCollectionDetailView.as_view(),
        name="idea-collection-detail",
    ),
]
