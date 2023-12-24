from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import AnimeReview, EpisodeReview


class AnimeReviewForm(forms.ModelForm):
    """Form of anime reviews"""

    class Meta:
        model = AnimeReview
        fields = ("text",)


class EpisodeReviewForm(forms.ModelForm):
    """Form of episode reviews"""

    class Meta:
        model = EpisodeReview
        fields = ("text",)


class SingupForm(UserCreationForm):
    """Form of singup user"""

    class Meta(UserCreationForm.Meta):
        model = User
