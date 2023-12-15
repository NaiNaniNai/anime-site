from django import template
from django.db.models import Q

from datetime import datetime

from anime.models import Category, Anime, AnimeReview

register = template.Library()


@register.simple_tag()
def get_categories():
    """Output all categories"""

    return Category.objects.all()


@register.inclusion_tag("tags/last_anime.html")
def get_last_anime(count):
    """Output the last anime"""

    anime = Anime.objects.filter(is_draft=False).order_by("-id")[:count]
    context = {"last_anime": anime}
    return context


@register.inclusion_tag("tags/trend_anime.html")
def get_trend_anime():
    """Output the trend anime"""

    month = datetime.now().month
    anime = Anime.objects.filter(
        Q(is_draft=False) & Q(created_at__month__range=[f"{month-1}", f"{month}"])
    ).order_by("-views")[:3]
    context = {"trend_anime": anime}
    return context


@register.inclusion_tag("tags/popular_anime.html")
def get_popular_anime():
    """Output the popular anime"""

    anime = Anime.objects.filter(is_draft=False).order_by("-views")[:3]
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
            Q(is_draft=False) & Q(created_at__month__range=[f"{month - 1}", f"{month}"])
        ).order_by("-views")[:1]
    )
    popular_anime = list(Anime.objects.filter(is_draft=False).order_by("-views")[:1])
    last_anime = list(Anime.objects.filter(is_draft=False).order_by("-id")[:1])
    hero_section_anime = trend_anime + popular_anime + last_anime
    context = {
        "animes": hero_section_anime,
    }
    return context
