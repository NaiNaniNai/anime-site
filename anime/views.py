import openpyxl
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic.base import View
from django.views.generic import ListView, DetailView, FormView

from project_root.settings import BASE_DIR


from .models import Anime, Studio, Category, Vote, Episode, Account, FollowingAnime
from .forms import AnimeReviewForm, EpisodeReviewForm, SingupForm


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
        user_vote = None

        if sum(votes):
            anime_rating = sum(votes) / len(votes)

        if self.request.user.id:
            user_vote = self.object.vote_set.filter(
                user=self.request.user, anime=self.object
            ).first()
            user_rating = ()

        if user_vote:
            user_rating = range(user_vote.rating + 1)
            context.update(user_rating=user_rating)

        context.update(anime_rating=anime_rating)

        context["similar_anime"] = (
            Anime.objects.filter(
                Q(is_draft=False)
                & (
                    Q(category_id=self.object.category.id)
                    | Q(genres__in=self.object.genres.all())
                )
            )
            .exclude(id=self.object.id)
            .distinct()[:3]
        )

        return context

    def get(self, request, *args, **kwargs):
        anime = self.get_object()
        anime.autoincrement_views()
        return super().get(request, *args, **kwargs)


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


class About(View):
    """Output about us"""

    def get(self, request):
        return render(request, "about.html")


class AccountDetail(View):
    """Detail of account"""

    def get(self, request, slug):
        account = Account.objects.filter(slug=slug).first()
        user = User.objects.filter(username=account.user.username).first()
        follows = user.following_anime.all()

        context = {
            "account": account,
            "follows": follows,
        }

        return render(request, "profile.html", context)


class LoginView(View):
    """Login in anime site"""

    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(reverse("anime_list"))
        else:
            return JsonResponse(
                {
                    "Error": "Ошибка или в имени или в пароле",
                }
            )


def logout_view(request):
    """Logout from anime site"""

    logout(request)
    return redirect(reverse("anime_list"))


class SingupView(FormView):
    """Singup in anime site"""

    form_class = SingupForm
    template_name = "signup.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


def handle_uploaded_file(f):

    with open(f"{BASE_DIR}/media/avatars/{f.name}", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)


class EditAccountView(View):
    """Edit anime account"""

    def get(self, request, user_slug):
        account = Account.objects.filter(slug=user_slug).first()
        context = {
            "account": account,
        }
        return render(request, "account_edit.html", context)

    def post(self, request, user_slug):
        account = Account.objects.filter(slug=user_slug).first()
        if request.FILES.get("avatar"):
            handle_uploaded_file(request.FILES["avatar"])
            avatar = request.FILES["avatar"]
        else:
            avatar = account.image
        if request.POST.get("email"):
            email = request.POST.get("email")
        else:
            email = account.user.email
        if request.POST.get("last_name"):
            last_name = request.POST.get("last_name")
        else:
            last_name = account.user.last_name
        if request.POST.get("first_name"):
            first_name = request.POST.get("first_name")
        else:
            first_name = account.user.first_name
        if request.POST.get("date_of_birth"):
            date_of_birth = request.POST.get("date_of_birth")
        else:
            date_of_birth = account.date_of_birth

        Account.objects.update_or_create(
            user=request.user,
            defaults={
                "date_of_birth": date_of_birth,
                "image": avatar,
            },
        )

        User.objects.filter(username=account).update(
            last_name=last_name, first_name=first_name, email=email
        )

        return redirect(reverse("account_detail", kwargs={"slug": user_slug}))


class ResetPasswordView(View):
    """Reset password of user"""

    def get(self, request):
        return render(request, "reset_password.html")

    def post(self, request):
        username = request.POST.get("username")
        email = request.POST.get("email")
        new_password = request.POST.get("new_password")
        user = User.objects.filter(username=username).first()
        if user.email == email:
            if new_password:
                user.set_password(new_password)
                user.save()

        return redirect(reverse("login"))


def get_following_anime(request, anime_slug):
    """Add following anime on user"""

    if request.method == "GET":
        anime = Anime.objects.filter(slug=anime_slug).first()
        user = request.user
        if FollowingAnime.objects.filter(user_id=user.id, anime_id=anime.id):
            FollowingAnime.objects.filter(user=user, anime_id=anime.id).delete()
        else:
            FollowingAnime.objects.filter(user=user).create(
                user_id=user.id, anime_id=anime.id
            )
        return redirect(reverse("anime_detail", kwargs={"slug": anime_slug}))


class ExportToExcelView(View):
    """Export to excel"""

    def get(self, requset):
        return render(requset, "export_to_excel.html")

    def post(self, request):
        query = Anime.objects.filter(is_draft=False).order_by("id")
        title = request.POST.get("title")
        type = request.POST.get("type")

        if title:
            query = query.filter(title__icontains=title)

        if type:
            query = query.filter(type=type)

        fields = [field.name for field in Anime._meta.fields]

        workbook = openpyxl.Workbook()
        worksheet = workbook.active
        worksheet.append(fields)
        animes = query.values_list(*fields)

        for anime in animes:
            worksheet.append(anime)

        response = HttpResponse(content_type="application/ms-excel")
        response["Content-Disposition"] = "attachment; filename=result.xlsx"
        workbook.save(response)

        return response
