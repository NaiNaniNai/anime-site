from django import template

from datetime import datetime
import secrets

from anime.models import Category, Anime, AnimeReview

register = template.Library()


@register.simple_tag()
def get_categories():
    """Output all categories"""

    return Category.objects.all()


@register.inclusion_tag("tags/last_anime.html")
def get_last_anime(count):
    """Output the last anime"""

    anime = Anime.objects.filter(is_draft=False, type="Тв-сериал").order_by("-id")[
        :count
    ]
    context = {"last_anime": anime}
    return context


@register.inclusion_tag("tags/trend_anime.html")
def get_trend_anime():
    """Output the trend anime"""

    month = datetime.now().month
    anime = Anime.objects.filter(
        is_draft=False,
        type="Тв-сериал",
        created_at__month__range=[f"{month - 1}", f"{month}"],
    ).order_by("-views")[:3]
    context = {"trend_anime": anime}
    return context


@register.inclusion_tag("tags/popular_anime.html")
def get_popular_anime():
    """Output the popular anime"""

    anime = Anime.objects.filter(is_draft=False, type="Тв-сериал").order_by("-views")[
        :3
    ]
    context = {"popular_anime": anime}
    return context


@register.inclusion_tag("tags/the_last_reviewed_anime.html")
def get_last_reviewed_anime():
    """Output the last reviewed anime"""

    reviews = AnimeReview.objects.select_related("anime").order_by("-created_at")
    animes = []

    for review in reviews:
        anime = review.anime

        if anime not in animes:
            animes.append(anime)

    context = {"last_reviewed_anime": animes}
    return context


@register.inclusion_tag("tags/hero_section.html")
def get_hero_section():
    """Output the hero section"""

    month = datetime.now().month
    trend_anime = list(
        Anime.objects.filter(
            is_draft=False,
            type="Тв-сериал",
            created_at__month__range=[f"{month - 1}", f"{month}"],
        ).order_by("-views")[:1]
    )
    popular_anime = list(
        Anime.objects.filter(is_draft=False, type="Тв-сериал").order_by("-views")[:1]
    )
    last_anime = list(
        Anime.objects.filter(is_draft=False, type="Тв-сериал").order_by("-id")[:1]
    )
    hero_section_anime = trend_anime + popular_anime + last_anime
    context = {
        "animes": hero_section_anime,
    }
    return context


@register.inclusion_tag("tags/popular_anime_in_sidebar.html")
def get_popular_anime_in_sidebar():
    """Output the anime with types tv, movie, ova"""

    tv_anime = Anime.objects.filter(is_draft=False, type="Тв-сериал").order_by(
        "-views"
    )[:3]
    movie_anime = Anime.objects.filter(is_draft=False, type="Фильм").order_by("-views")[
        :3
    ]
    ova_anime = Anime.objects.filter(is_draft=False, type="Oва").order_by("-views")[:3]
    context = {
        "tv_anime": tv_anime,
        "movie_anime": movie_anime,
        "ova_anime": ova_anime,
    }
    return context


@register.simple_tag()
def get_random_anime():
    """Get a random anime"""

    return secrets.choice(Anime.objects.filter(is_draft=False))
