from django.urls import path

from . import views


urlpatterns = [
    path("", views.AnimeViews.as_view()),
    path("<slug:slug>/", views.AnimeDetailViews.as_view(), name="anime_detail"),
]
