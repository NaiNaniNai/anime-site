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
    path("about/", views.About.as_view(), name="about"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("singup/", views.SingupView.as_view(), name="singup"),
    path("logout/", views.logout_view, name="logout"),
    path("reset_password/", views.ResetPasswordView.as_view(), name="reset_password"),
    path("users/<slug:slug>/", views.AccountDetail.as_view(), name="account_detail"),
    path(
        "users/<slug:user_slug>/edit",
        views.EditAccountView.as_view(),
        name="account_edit",
    ),
    path("export/", views.ExportToExcelView.as_view(), name="export"),
    path("<slug:slug>/", views.AnimeDetailViews.as_view(), name="anime_detail"),
    path("<slug:anime_slug>/watch/", views.EpisodeList.as_view(), name="episode_list"),
    path(
        "<slug:anime_slug>/watch/<slug:episode_slug>",
        views.EpisodeDetail.as_view(),
        name="episode_detail",
    ),
    path("<slug:anime_slug>/add_following", views.get_following_anime, name="follow"),
]
