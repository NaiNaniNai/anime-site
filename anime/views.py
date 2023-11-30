from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic.base import View
from django.views.generic import ListView, DetailView

from .models import Anime, Studio, Vote
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

    def post(self, request, slug):
        rating = request.POST.get("rating")
        anime = Anime.objects.filter(slug=slug).first()
        Vote.objects.update_or_create(
            user=request.user,
            anime=anime,
            defaults={
                "rating": rating,
            },
        )

        return redirect(reverse("anime_detail", kwargs={"slug": anime.slug}))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        votes = self.object.vote_set.values_list("rating", flat=True)
        anime_rating = 0

        if sum(votes):
            anime_rating = sum(votes) / len(votes)

        user_vote = self.object.vote_set.filter(
            user=self.request.user, anime=self.object
        ).first()
        user_rating = ()

        if user_vote:
            user_rating = range(user_vote.rating + 1)

        context.update(user_rating=user_rating, anime_rating=anime_rating)

        return context


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

    def get_context_data(self, **kwargs):
        context = super(StudioViews, self).get_context_data()
        context["filter_anime"] = self.object.animes.filter(is_draft=False)
        return context
