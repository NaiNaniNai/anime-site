from django.urls import path

from anime import views


urlpatterns = [
    path("", views.AnimeViews.as_view(), name="anime_list"),
    path("result/", views.Search.as_view(), name="search"),
    path("studio/<str:slug>/", views.StudioViews.as_view(), name="studio_detail"),
    path("category/", views.CategoryViews.as_view(), name="category_list"),
    path(
        "category/<str:slug>/",
        views.CategoryDetailViews.as_view(),
        name="category_detail",
    ),
    path("<slug:slug>/", views.AnimeDetailViews.as_view(), name="anime_detail"),
    path("<slug:anime_slug>/watch/", views.EpisodeList.as_view(), name="episode_list"),
    path(
        "<slug:anime_slug>/watch/<slug:episode_slug>",
        views.EpisodeDetail.as_view(),
        name="episode_detail",
    ),
]
