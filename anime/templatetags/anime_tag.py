from django import template
from django.db.models import Q

from datetime import datetime

from anime.models import Category, Anime

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
    ).order_by("-views")
    context = {"trend_anime": anime}
    return context


@register.inclusion_tag("tags/popular_anime.html")
def get_popular_anime():
    """Output the popular anime"""

    anime = Anime.objects.filter(is_draft=False).order_by("-views")
    context = {"popular_anime": anime}
    return context
