from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User

from anime.choices import STATUS_CHOICES, TYPE_CHOICES, QUALITY_CHOICES


class Account(models.Model):
    """Model of account"""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="account",
        verbose_name="Пользователь",
        unique=True,
    )
    date_of_birth = models.DateField(verbose_name="Дата рождения")
    image = models.ImageField(upload_to="avatars/", verbose_name="Аватарка")

    class Meta:
        verbose_name = "Аккаунт"
        verbose_name_plural = "Аккаунты"

    def __str__(self) -> str:
        return f"{self.user}"


class Studio(models.Model):
    """Model for studio"""

    name = models.CharField(max_length=128, verbose_name="Название")
    slug = models.SlugField(max_length=128, verbose_name="Слаг")
    description = models.CharField(max_length=4096, verbose_name="Описание")
    image = models.ImageField(upload_to="posters/", verbose_name="Постер", null=True)

    class Meta:
        verbose_name = "Студия"
        verbose_name_plural = "Студии"

    def __str__(self) -> str:
        return self.name


class Genre(models.Model):
    """Model for genre"""

    name = models.CharField(max_length=128, verbose_name="Название")
    slug = models.SlugField(max_length=128, verbose_name="Слаг")
    description = models.CharField(max_length=4096, verbose_name="Описание")

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    """Model for category"""

    name = models.CharField(max_length=128, verbose_name="Название")
    slug = models.SlugField(max_length=128, verbose_name="Слаг")
    description = models.CharField(max_length=4096, verbose_name="Описание")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self) -> str:
        return self.name


class Anime(models.Model):
    """Model for anime"""

    title = models.CharField(max_length=256, verbose_name="Название")
    japan_title = models.CharField(max_length=256, verbose_name="Японское назввание")
    slug = models.SlugField(max_length=256, verbose_name="Слаг")
    description = models.CharField(max_length=4096, verbose_name="Описание")
    type = models.CharField(
        max_length=64, choices=TYPE_CHOICES, verbose_name="Тип показа"
    )
    status = models.CharField(
        max_length=64, choices=STATUS_CHOICES, verbose_name="Статус"
    )
    studio = models.ForeignKey(
        Studio, on_delete=models.PROTECT, related_name="animes", verbose_name="Студия"
    )
    genres = models.ManyToManyField(Genre, verbose_name="Жанры")
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="animes",
        verbose_name="Категория",
    )
    start_date = models.DateField(verbose_name="Дата начала")
    end_date = models.DateField(verbose_name="Дата окончания", blank=True, null=True)
    released_episodes = models.IntegerField(verbose_name="Вышедшие эпизоды")
    planned_episodes = models.IntegerField(verbose_name="Запланируемые эпизоды")
    duration = models.IntegerField(
        verbose_name="Длительность в минутах (0, если неизвестно)",
        blank=True,
        null=True,
    )
    quality = models.CharField(
        max_length=128,
        choices=QUALITY_CHOICES,
        verbose_name="Качество",
        default="Пока не объявлено",
    )
    views = models.IntegerField(verbose_name="Просмотры", blank=True, null=True)
    poster = models.ImageField(upload_to="posters/", verbose_name="Постер")
    poster_for_main_page = models.ImageField(
        upload_to="posters_main/", verbose_name="Постер на главной странице"
    )
    created_at = models.DateField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateField(
        auto_now=True, verbose_name="Дата обновления", blank=True
    )
    is_draft = models.BooleanField(verbose_name="Черновик", default=False)

    class Meta:
        verbose_name = "Аниме"
        verbose_name_plural = "Аниме"

    def __str__(self) -> str:
        return f"{self.title} - {self.japan_title}"

    def get_review(self):
        return self.animereview_set.filter(parent__isnull=True)

    def autoincrement_views(self):
        self.views += 1
        self.save(update_fields=["views"])


class Episode(models.Model):
    """Model for episode"""

    title = models.CharField(max_length=128, verbose_name="Название")
    slug = models.SlugField(max_length=128, verbose_name="Слаг")
    anime = models.ForeignKey(
        Anime, on_delete=models.CASCADE, related_name="episodes", verbose_name="Аниме"
    )
    description = models.CharField(
        max_length=4096, verbose_name="Описание серии", blank=True
    )
    video = models.FileField(upload_to="episodes/", verbose_name="Эпизод")
    created_at = models.DateField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateField(
        auto_now=True, verbose_name="Дата обновления", blank=True
    )

    class Meta:
        verbose_name = "Эпизод"
        verbose_name_plural = "Эпизоды"

    def __str__(self) -> str:
        return f"{self.anime} - {self.title}"

    def get_review(self):
        return self.episodereview_set.filter(parent__isnull=True)


class AnimeShots(models.Model):
    """Model for shots for anime"""

    title = models.CharField(max_length=128, verbose_name="Заголовок")
    description = models.CharField(max_length=1024, verbose_name="Описание")
    image = models.ImageField(upload_to="anime_shots/", verbose_name="Изображение")
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, verbose_name="Аниме")

    class Meta:
        verbose_name = "Кадр из аниме"
        verbose_name_plural = "Кадры из аниме"

    def __str__(self) -> str:
        return f"{self.anime} - {self.title}"


class EpisodeShots(models.Model):
    """Model for shots for episode"""

    title = models.CharField(max_length=128, verbose_name="Заголовок")
    description = models.CharField(max_length=1024, verbose_name="Описание")
    image = models.ImageField(upload_to="episode_image/", verbose_name="Изображение")
    episode = models.ForeignKey(
        Episode, on_delete=models.CASCADE, verbose_name="Эпизод"
    )

    class Meta:
        verbose_name = "Кадр из эпизода"
        verbose_name_plural = "Кадры из эпизодов"

    def __str__(self) -> str:
        return f"{self.episode} - {self.title}"


class Vote(models.Model):
    """Model for vote"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, verbose_name="Аниме")
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=0,
        verbose_name="Рейтинг",
    )
    created_at = models.DateField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateField(
        auto_now=True, blank=True, verbose_name="Дата обновления"
    )

    class Meta:
        verbose_name = "Оценка"
        verbose_name_plural = "Оценки"

    def __str__(self) -> str:
        return f"{self.user} - {self.anime}"


class FollowingAnime(models.Model):
    """Model for following anime"""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, verbose_name="Аниме")
    created_at = models.DateField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateField(
        auto_now=True, verbose_name="Дата обновления", blank=True
    )

    class Meta:
        verbose_name = "Отслеживаемое аниме"
        verbose_name_plural = "Отслеживаемые аниме"

    def __str__(self) -> str:
        return f"{self.user} - {self.anime}"


class AnimeReview(models.Model):
    """Model for anime commentary"""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, verbose_name="Аниме")
    text = models.CharField(max_length=512, verbose_name="Текст")
    is_spoiler = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateField(
        auto_now=True, verbose_name="Дата обновления", blank=True
    )
    parent = models.ForeignKey(
        "self",
        verbose_name="Родитель",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Комментарий к аниме"
        verbose_name_plural = "Комментарии к аниме"

    def __str__(self) -> str:
        return f"{self.user} - {self.anime} - {self.text}"


class EpisodeReview(models.Model):
    """Model for episode commentary"""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    episode = models.ForeignKey(
        Episode, on_delete=models.CASCADE, verbose_name="Эпизод"
    )
    text = models.CharField(max_length=512, verbose_name="Текст")
    is_spoiler = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateField(
        auto_now=True, verbose_name="Дата обновления", blank=True
    )
    parent = models.ForeignKey(
        "self",
        verbose_name="Родитель",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Комментарий к эпизоду"
        verbose_name_plural = "Комментарии к эпизодам"

    def __str__(self) -> str:
        return f"{self.episode} - {self.user} - {self.text}"
