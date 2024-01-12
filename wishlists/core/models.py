from uuid import uuid4
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext, gettext_lazy as _

from core import managers


class TrackedModel(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, verbose_name=_("ID"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))

    class Meta:
        abstract = True


class User(TrackedModel, AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name=_("email"))

    is_active = models.BooleanField(
        default=True,
        help_text=_("Only active users are able to log in."),
        verbose_name=_("is active"),
    )
    is_staff = models.BooleanField(
        default=False,
        help_text=_("Staff users can access the admin site."),
        verbose_name=_("is staff"),
    )
    is_superuser = models.BooleanField(
        default=False,
        help_text=_("Super users are implicitly granted all permissions."),
        verbose_name=_("is superuser"),
    )

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"

    objects = managers.UserManager()

    class Meta:
        ordering = ("id",)
        verbose_name = _("user")
        verbose_name_plural = _("users")


class IdeaList(TrackedModel):
    """
    A list of gift ideas.
    """

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="idea_lists",
        related_query_name="idea_list",
        verbose_name=_("owner"),
    )

    name = models.CharField(
        blank=False, null=False, max_length=100, verbose_name=_("name")
    )

    class Meta:
        ordering = ("created_at",)
        verbose_name = _("idea list")
        verbose_name_plural = _("idea lists")

    def __str__(self) -> str:
        return self.name


class GiftIdea(TrackedModel):
    """
    A gift idea.
    """

    collection = models.ForeignKey(
        IdeaList,
        on_delete=models.CASCADE,
        related_name="ideas",
        related_query_name="idea",
        verbose_name=_("idea collection"),
        help_text=_("The collection that this idea belongs to."),
    )

    description = models.TextField(
        blank=True, null=False, verbose_name=_("description")
    )
    link = models.URLField(
        blank=False,
        null=True,
        verbose_name=_("link"),
        help_text=_("A link with more information about the idea."),
    )

    class Meta:
        ordering = ("created_at",)
        verbose_name = _("gift idea")
        verbose_name_plural = _("gift ideas")

    def clean(self) -> None:
        super().clean()

        if not self.description and not self.link:
            raise ValidationError(
                gettext("A gift idea must have at least a description or link.")
            )

    @property
    def display_text(self):
        if self.description:
            return self.description

        return self.link
