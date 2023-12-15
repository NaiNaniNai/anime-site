from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic.base import View
from django.views.generic import ListView, DetailView

from .models import Anime, Studio, Category, Vote, Episode
from .forms import AnimeReviewForm, EpisodeReviewForm


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
        if request.POST.get("rating"):
            rating = request.POST.get("rating")
            anime = Anime.objects.filter(slug=slug).first()
            Vote.objects.update_or_create(
                user=request.user,
                anime=anime,
                defaults={
                    "rating": rating,
                },
            )

        elif request.POST.get("text"):
            form = AnimeReviewForm(request.POST)
            anime = Anime.objects.get(slug=slug)
            is_spoiler = request.POST.get("have_spoiler") == "on"

            if form.is_valid():
                form = form.save(commit=False)
                form.user = request.user
                if request.POST.get("parent"):
                    form.parent_id = int(request.POST.get("parent"))
                if is_spoiler:
                    form.is_spoiler = is_spoiler
                form.anime_id = anime.pk
                form.save()

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

        context["similar_anime"] = (
            Anime.objects.filter(
                Q(is_draft=False)
                & (
                    Q(category_id=self.object.category.id)
                    | Q(genres__in=self.object.genres.all())
                )
            )
            .exclude(id=self.object.id)
            .distinct()
        )
        return context


class StudioViews(DetailView):
    """Detail of studio"""

    model = Studio
    slug_field = "slug"
    template_name = "studio.html"

    def get_context_data(self, **kwargs):
        context = super(StudioViews, self).get_context_data()
        context["filter_anime"] = self.object.animes.filter(is_draft=False)
        return context


class Search(ListView):
    """Search anime for title"""

    template_name = "search.html"
    context_object_name = "result"

    def get_queryset(self):
        q = self.request.GET.get("q").capitalize()
        return Anime.objects.filter(title__icontains=q)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = self.request.GET.get("q")
        return context


class CategoryViews(ListView):
    """List of category"""

    model = Category
    template_name = "category_list.html"
    queryset = Category.objects.all()


class CategoryDetailViews(DetailView):
    """Detail of category"""

    model = Category
    slug_field = "slug"
    template_name = "category_detail.html"

    def get_context_data(self, **kwargs):
        context = super(CategoryDetailViews, self).get_context_data()
        context["filter_anime"] = self.object.animes.filter(is_draft=False)
        return context


class EpisodeList(View):
    """List of episodes of anime"""

    def get(self, request, anime_slug):
        anime = (
            Anime.objects.prefetch_related("episodes").filter(slug=anime_slug).first()
        )
        episodes = anime.episodes.order_by("id")
        if not anime:
            return HttpResponse("Anime is not define")

        context = {
            "anime": anime,
            "episodes": episodes,
        }

        return render(request, "episode_list.html", context)


class EpisodeDetail(View):
    """Detail of episode"""

    def get(self, request, anime_slug, episode_slug):
        anime = (
            Anime.objects.prefetch_related("episodes").filter(slug=anime_slug).first()
        )
        object = anime.episodes.filter(slug=episode_slug).first()
        episodes = anime.episodes.order_by("id")
        index_current_episode = list(episodes.values_list("id", flat=True)).index(
            object.id
        )
        try:
            next_episode = episodes[index_current_episode + 1]
        except IndexError:
            next_episode = []
        try:
            last_episode = episodes[index_current_episode - 1]
        except ValueError:
            last_episode = []
        if not anime:
            return JsonResponse(
                {
                    "Error": "Аниме не найдено",
                }
            )

        if not object:
            return JsonResponse(
                {
                    "Error": "Эпизод не найден",
                }
            )

        context = {
            "anime": anime,
            "object": object,
            "episodes": episodes,
            "next_episode": next_episode,
            "last_episode": last_episode,
        }

        return render(request, "episode_detail.html", context)

    def post(self, request, anime_slug, episode_slug):
        form = EpisodeReviewForm(request.POST)
        episode = Episode.objects.get(slug=episode_slug, anime__slug=anime_slug)

        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            if request.POST.get("parent"):
                form.parent_id = int(request.POST.get("parent"))
            is_spoiler = request.POST.get("have_spoiler") == "on"
            if is_spoiler:
                form.is_spoiler = is_spoiler
            form.episode_id = episode.pk
            form.save()

        return redirect(
            reverse(
                "episode_detail",
                kwargs={"episode_slug": episode.slug, "anime_slug": anime_slug},
            )
        )
