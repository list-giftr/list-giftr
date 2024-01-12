# Generated by Django 5.0.1 on 2024-01-11 23:13

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_idealist"),
    ]

    operations = [
        migrations.CreateModel(
            name="GiftIdea",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="created at"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="updated at"),
                ),
                (
                    "description",
                    models.TextField(blank=True, verbose_name="description"),
                ),
                (
                    "link",
                    models.URLField(
                        help_text="A link with more information about the idea.",
                        null=True,
                        verbose_name="link",
                    ),
                ),
                (
                    "collection",
                    models.ForeignKey(
                        help_text="The collection that this idea belongs to.",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="ideas",
                        related_query_name="idea",
                        to="core.idealist",
                        verbose_name="idea collection",
                    ),
                ),
            ],
            options={
                "verbose_name": "gift idea",
                "verbose_name_plural": "gift ideas",
                "ordering": ("created_at",),
            },
        ),
    ]