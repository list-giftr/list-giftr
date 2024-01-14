from uuid import uuid4

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.db.models import F
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from core import managers


class TrackedModel(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, verbose_name=_("ID"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))

    class Meta:
        abstract = True


class User(TrackedModel, AbstractBaseUser, PermissionsMixin):  # noqa: DJ008
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


class IdeaCollection(TrackedModel):
    """
    A list of gift ideas.
    """

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="idea_collections",
        related_query_name="idea_collection",
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

    def get_absolute_url(self):
        return reverse("idea-collection-detail", kwargs={"pk": self.pk})


class GiftIdea(TrackedModel):
    """
    A gift idea.
    """

    collection = models.ForeignKey(
        IdeaCollection,
        on_delete=models.CASCADE,
        related_name="ideas",
        related_query_name="idea",
        verbose_name=_("idea collection"),
        help_text=_("The collection that this idea belongs to."),
    )

    name = models.CharField(
        blank=False, null=False, max_length=100, verbose_name=_("name")
    )
    description = models.TextField(
        blank=True, null=False, verbose_name=_("description")
    )
    link = models.URLField(  # noqa: DJ001 - Blank link doesn't make sense.
        blank=False,
        null=True,
        verbose_name=_("link"),
        help_text=_("A link with more information about the idea."),
    )
    mention_count = models.PositiveSmallIntegerField(
        null=False,
        default=1,
        verbose_name=_("mention count"),
        help_text=_("The number of times this gift idea has been brought up."),
    )

    class Meta:
        ordering = ("created_at",)
        verbose_name = _("gift idea")
        verbose_name_plural = _("gift ideas")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("gift-idea-detail", kwargs={"pk": self.pk})

    def increment_mention_count(self):
        """
        Increment the instance's ``mention_count`` by one.

        This is performed as a database operation. If callers need the
        updated value, they must call ``model.refresh_from_db()`` to
        see it.
        """
        self.mention_count = F("mention_count") + 1
        self.save()
