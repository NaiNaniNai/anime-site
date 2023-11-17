from django.urls import path

from . import views


urlpatterns = [
    path("", views.AnimeViews.as_view(), name="anime_list"),
    path("<slug:slug>/", views.AnimeDetailViews.as_view(), name="anime_detail"),
    path("review/<int:pk>/", views.AddReview.as_view(), name="add_review"),
]
