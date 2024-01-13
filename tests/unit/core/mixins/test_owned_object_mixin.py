from unittest import mock

import pytest
from core.mixins import OwnedObjectMixin


class MockParentView:
    def __init__(self, queryset):
        self.queryset = queryset

    def get_queryset(self):
        return self.queryset


class DefaultsView(OwnedObjectMixin, MockParentView):
    pass


class OverriddenView(OwnedObjectMixin, MockParentView):
    object_owner_field = "some_other_field"


@pytest.fixture()
def queryset():
    return mock.MagicMock(name="QuerySet")


def test_get_queryset_defaults(queryset):
    request = mock.MagicMock(spec="django.http.HttpRequest")
    request.user = mock.MagicMock(name="User")

    view = DefaultsView(queryset)
    view.request = request

    received = view.get_queryset()

    assert received == queryset.filter.return_value
    queryset.filter.assert_called_once_with(owner=request.user)


def test_get_queryset_custom_owner_field(queryset):
    request = mock.MagicMock(spec="django.http.HttpRequest")
    request.user = mock.MagicMock(name="User")

    view = OverriddenView(queryset)
    view.request = request

    received = view.get_queryset()

    assert received == queryset.filter.return_value
    queryset.filter.assert_called_once_with(some_other_field=request.user)
