from django.test import Client
from django.urls import reverse


def test_unauthenticated(client: Client):
    response = client.get("/")

    assert response.status_code == 200

    content = str(response.content)
    assert reverse("account_login") in content
    assert reverse("account_signup") in content
