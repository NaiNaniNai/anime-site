from django.http import HttpRequest
from django.shortcuts import render
from django.template.response import TemplateResponse
from django.views.generic.base import View
from django.views.generic import ListView, DetailView

from .models import Anime


class AnimeViews(ListView):
    """List of anime"""

    model = Anime
    queryset = Anime.objects.filter(is_draft=False)
    template_name = "anime_list.html"


class AnimeDetailViews(DetailView):
    """Detail of anime"""

    model = Anime
    slug_field = "slug"
    template_name = "anime_detail.html"
