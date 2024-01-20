from core.models import IdeaCollection, User
from django.test import Client
from django.urls import reverse_lazy

LIST_URL = reverse_lazy("idea-collection-list")


def test_not_authenticated(assert_login_redirect, client: Client):
    response = client.get(LIST_URL)

    assert_login_redirect(response, LIST_URL)


def test_no_idea_collections(authenticated_client: Client):
    response = authenticated_client.get(LIST_URL)

    assert response.status_code == 200


def test_only_owned_collections(authenticated_client: Client):
    other_user = User.objects.create_user(
        email="other@example.com", password="password"
    )
    collection = IdeaCollection.objects.create(
        owner=other_user, name="Other Collection"
    )

    response = authenticated_client.get(LIST_URL)

    assert response.status_code == 200
    assert collection.name not in str(response.content)


def test_multiple_collections(authenticated_client, normal_user):
    collections = [
        IdeaCollection.objects.create(owner=normal_user, name="First Collection"),
        IdeaCollection.objects.create(owner=normal_user, name="Second Collection"),
    ]

    response = authenticated_client.get(LIST_URL)

    assert response.status_code == 200

    content = str(response.content)

    for collection in collections:
        assert collection.name in content
        assert collection.get_absolute_url() in content
