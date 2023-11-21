from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic.base import View
from django.views.generic import ListView, DetailView

from .models import Anime, Studio
from .forms import AnimeReviewForm


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


class AddReview(View):
    """Add review of anime"""

    def post(self, request, pk):
        form = AnimeReviewForm(request.POST)
        anime = Anime.objects.get(id=pk)

        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
            form.anime_id = pk
            form.save()

        return redirect(reverse("anime_detail", kwargs={"slug": anime.slug}))


class StudioViews(DetailView):
    """Detail of studio"""

    model = Studio
    slug_field = "name"
    template_name = "studio.html"
