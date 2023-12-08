from django import forms

from .models import AnimeReview, EpisodeReview


class AnimeReviewForm(forms.ModelForm):
    """Form of anime reviews"""

    class Meta:
        model = AnimeReview
        fields = ("text",)


class EpisodeReviewForm(forms.ModelForm):
    class Meta:
        model = EpisodeReview
        fields = ("text",)
