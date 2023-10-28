from django.shortcuts import render
from django.views.generic.base import View

from .models import Anime


class AnimeViews(View):
    """Список аниме"""

    def get(self, request):
        animes = Anime.objects.filter(is_draft=False)
        return render(request, "anime/anime_list.html", {"anime_list": animes})
