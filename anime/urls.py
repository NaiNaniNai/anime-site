from django.urls import path

from anime import views


urlpatterns = [
    path("", views.AnimeViews.as_view(), name="anime_list"),
    path("result/", views.Search.as_view(), name="search"),
    path("<slug:slug>/", views.AnimeDetailViews.as_view(), name="anime_detail"),
    path("review/<int:pk>/", views.AddReview.as_view(), name="add_review"),
    path("studio/<str:slug>/", views.StudioViews.as_view(), name="studio_detail"),
]
