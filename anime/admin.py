from django.contrib import admin

from anime.models import (
    Studio,
    Genre,
    Category,
    Anime,
    Vote,
    FollowingAnime,
    Episode,
    AnimeReview,
    EpisodeReview,
    AnimeShots,
    EpisodeShots,
)


@admin.register(Studio)
class StudioAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


@admin.register(AnimeShots)
class AnimeShotsAdmin(admin.ModelAdmin):
    pass


@admin.register(EpisodeShots)
class EpisodeShotsAdmin(admin.ModelAdmin):
    pass


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    pass


@admin.register(FollowingAnime)
class FollowingAnimeAdmin(admin.ModelAdmin):
    pass


@admin.register(AnimeReview)
class AnimeReviewAdmin(admin.ModelAdmin):
    pass


@admin.register(EpisodeReview)
class EpisodeReviewAdmin(admin.ModelAdmin):
    pass
