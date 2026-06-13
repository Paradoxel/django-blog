from django.urls import path

from . import views
from .feeds import LatestPostsFeed

app_name = "blog"

urlpatterns = [
    path("", views.BlogView.as_view(), name="index"),
    path("category/<slug:slug>/", views.BlogView.as_view(), name="category"),
    path("tag/<slug:slug>/", views.BlogView.as_view(), name="tag"),
    path('author/<int:pk>/',views.BlogView.as_view(),name='author'),
    path("feed/", LatestPostsFeed(), name="feed"),
    path("<slug:slug>/", views.PostDetailView.as_view(), name="detail"),
]