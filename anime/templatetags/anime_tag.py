from django import template

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
