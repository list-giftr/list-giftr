from django.urls import path

from core import views

urlpatterns = [
    path(
        "gift-idea/<uuid:pk>",
        views.GiftIdeaDetailView.as_view(),
        name="gift-idea-detail",
    ),
    path("ideas/", views.IdeaListsView.as_view(), name="idea-lists"),
    path(
        "ideas/<uuid:pk>/", views.IdeaListDetailView.as_view(), name="idea-list-detail"
    ),
]
