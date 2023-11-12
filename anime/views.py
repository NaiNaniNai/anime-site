from django.http import HttpRequest
from django.shortcuts import render
from django.template.response import TemplateResponse
from django.views.generic.base import View

from .models import Anime


class AnimeViews(View):
    """List of anime"""

    def get(self, request: HttpRequest) -> TemplateResponse:
        animes = Anime.objects.filter(is_draft=False)
        context = {"anime_list": animes}
        return render(request, "anime/templates/anime_list.html", context)
