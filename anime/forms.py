from django import forms

from .models import AnimeReview


class AnimeReviewForm(forms.ModelForm):
    """Form of anime reviews"""

    class Meta:
        model = AnimeReview
        fields = ("text",)
