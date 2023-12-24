from django.contrib import admin
from django.utils.safestring import mark_safe

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
    Account,
)


@admin.register(Studio)
class StudioAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("name",)
    ordering = ("id",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("name",)
    ordering = ("id",)

    prepopulated_fields = {"slug": ("name",)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("name",)
    ordering = ("id",)

    prepopulated_fields = {"slug": ("name",)}


class AnimeReviewInLine(admin.TabularInline):
    model = AnimeReview
    extra = 1


class AnimeShotsInLine(admin.TabularInline):
    model = AnimeShots
    extra = 1
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="150" height="auto"')

    get_image.short_description = "Изображение"  # type: ignore


@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "japan_title",
        "get_poster_for_main_page",
        "is_draft",
    )
    list_display_links = ("title", "japan_title")
    list_filter = ("genres", "studio")
    search_fields = ("title", "category__name")
    ordering = ("id",)
    inlines = [AnimeShotsInLine, AnimeReviewInLine]
    save_on_top = True
    save_as = True
    list_editable = ("is_draft",)
    actions = ["mark_as_undraft", "mark_as_draft"]
    fieldsets = (
        (
            "Главное",
            {
                "fields": (
                    ("title", "updated_at", "japan_title", "description", "slug"),
                )
            },
        ),
        ("Тип, статус и студия", {"fields": (("type", "status", "studio"),)}),
        ("Категория и жанры", {"fields": (("category", "genres"),)}),
        ("Даты", {"fields": (("start_date", "end_date"),)}),
        (
            "Эпизоды",
            {
                "fields": (
                    ("released_episodes", "planned_episodes", "duration", "quality"),
                )
            },
        ),
        (
            "Просмотры и постер",
            {
                "fields": (
                    (
                        "views",
                        "poster",
                        "poster_for_main_page",
                        "get_poster_for_main_page",
                    ),
                )
            },
        ),
        ("Опции", {"fields": (("is_draft"),)}),
    )
    readonly_fields = ("get_poster_for_main_page", "updated_at")

    prepopulated_fields = {"slug": ("title",)}

    def get_poster_for_main_page(self, obj):
        return mark_safe(
            f'<img src={obj.poster_for_main_page.url} width="100" height="120"'
        )

    get_poster_for_main_page.short_description = "Постер на главной странице"  # type: ignore

    def mark_as_undraft(self, request, queryset):
        row_update = queryset.update(is_draft=False)
        message = (
            f"{row_update} запись была обновлена"
            if row_update == 1
            else f"{row_update} записей было обновлено"
        )
        self.message_user(request, f"{message}")

    def mark_as_draft(self, request, queryset):
        row_update = queryset.update(is_draft=True)
        message = (
            f"{row_update} запись была обновлена"
            if row_update == 1
            else f"{row_update} записей было обновлено"
        )
        self.message_user(request, f"{message}")

    mark_as_undraft.short_description = "Убрать отметку черновика"  # type: ignore
    mark_as_undraft.allowed_permission = ("change",)  # type: ignore

    mark_as_draft.short_description = "Отметить как черновик"  # type: ignore
    mark_as_draft.allowed_permission = ("change",)  # type: ignore


class EpisodeReviewInLine(admin.TabularInline):
    model = EpisodeReview
    extra = 1


class EpisodeShotsInLine(admin.TabularInline):
    model = EpisodeShots
    extra = 1
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="150" height="auto"')

    get_image.short_description = "Изображение"  # type: ignore


@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "anime",
    )
    list_display_links = ("title",)
    ordering = (
        "anime",
        "title",
    )
    search_fields = ("title", "anime__title")
    inlines = [EpisodeShotsInLine, EpisodeReviewInLine]
    save_on_top = True
    save_as = True
    prepopulated_fields = {"slug": ("title",)}


@admin.register(AnimeShots)
class AnimeShotsAdmin(admin.ModelAdmin):
    list_display = ("title", "anime")
    list_display_links = ("title",)
    ordering = ("title",)
    search_fields = ("title", "anime__title")


@admin.register(EpisodeShots)
class EpisodeShotsAdmin(admin.ModelAdmin):
    list_display = ("title", "episode")
    list_display_links = ("title",)
    ordering = ("title",)
    search_fields = ("title", "episode__title")


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "anime", "rating")
    list_display_links = ("id",)
    ordering = ("id",)
    search_fields = ("user", "anime__tile")


@admin.register(FollowingAnime)
class FollowingAnimeAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "anime")
    list_display_links = ("id",)
    ordering = ("id",)
    search_fields = ("user", "anime__tile")


@admin.register(AnimeReview)
class AnimeReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "anime", "text", "is_spoiler")
    list_display_links = ("id", "user", "anime", "text")
    ordering = ("id",)
    readonly_fields = ("user", "anime")
    search_fields = ("user", "anime__title")
    list_editable = ("is_spoiler",)
    actions = ["publish", "mark_as_spoiler"]

    def mark_as_unspoiler(self, request, queryset):
        row_update = queryset.update(is_spoiler=False)
        message = (
            f"{row_update} запись была обновлена"
            if row_update == 1
            else f"{row_update} записей было обновлено"
        )
        self.message_user(request, f"{message}")

    def mark_as_spoiler(self, request, queryset):
        row_update = queryset.update(is_spoiler=True)
        message = (
            f"{row_update} запись была обновлена"
            if row_update == 1
            else f"{row_update} записей было обновлено"
        )
        self.message_user(request, f"{message}")

    mark_as_unspoiler.short_description = "Убрать отметку спойлера"  # type: ignore
    mark_as_unspoiler.allowed_permission = ("change",)  # type: ignore

    mark_as_spoiler.short_description = "Отметить как спойлер"  # type: ignore
    mark_as_spoiler.allowed_permission = ("change",)  # type: ignore


@admin.register(EpisodeReview)
class EpisodeReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "episode", "text", "is_spoiler")
    list_display_links = ("id", "user", "episode", "text")
    ordering = ("id",)
    readonly_fields = ("user", "episode")
    search_fields = ("user", "episode__title")
    list_editable = ("is_spoiler",)


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
    )
    list_display_links = (
        "id",
        "user",
    )
    ordering = ("id",)
    search_fields = ("user",)

    fieldsets = (
        (
            "Главное",
            {
                "fields": (
                    (
                        "user",
                        "slug",
                        "image",
                        # "get_avatar",
                    ),
                    ("date_of_birth",),
                )
            },
        ),
    )

    # def get_avatar(self, obj):
    #     return mark_safe(f'<img src={obj.image.url} width="100" height="120"')

    # readonly_fields = ("get_avatar",)
    # prepopulated_fields = {"slug": ("user__id",)}
    # get_avatar.short_description = "Аватарка"  # type: ignore
