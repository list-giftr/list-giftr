import pytest
from core.models import User
from django.http import HttpResponse
from django.test import Client
from django.urls import reverse


@pytest.fixture(scope="session")
def assert_login_redirect():
    def test_func(response: HttpResponse, next_url: str):
        expected_location = f"{reverse('account_login')}?next={next_url}"

        assert response.status_code == 302
        assert response.headers.get("Location") == expected_location

    return test_func


@pytest.fixture(scope="session")
def normal_user_credentials():
    return "test@example.com", "password"


@pytest.fixture()
def normal_user(db, normal_user_credentials) -> User:
    email, password = normal_user_credentials

    user = User.objects.create_user(email=email, password=password)

    return user


@pytest.fixture()
def authenticated_client(client: Client, normal_user) -> Client:
    client.force_login(normal_user)

    return client
