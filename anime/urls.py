from django.urls import path

from . import views


urlpatterns = [path("", views.AnimeViews.as_view())]
