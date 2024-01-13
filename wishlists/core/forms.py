from django import forms
from django.forms import ModelForm

from core import models


class GiftIdeaForm(ModelForm):
    class Meta:
        model = models.GiftIdea
        fields = ["name", "description", "link"]
        widgets = {"description": forms.Textarea(attrs={"rows": 5})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["link"].required = False


class GiftIdeaUpdateForm(GiftIdeaForm):
    class Meta(GiftIdeaForm.Meta):
        fields = ["name", "description", "link", "mention_count"]
