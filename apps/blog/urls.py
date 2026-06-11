from django.urls import path

from . import views

app_name = "blog"

urlpatterns = [
    path("", views.BlogView.as_view(), name="index"),
    path("category/<slug:slug>/", views.BlogView.as_view(), name="category"),
    path("tag/<slug:slug>/", views.BlogView.as_view(), name="tag"),
    path("<slug:slug>/", views.PostDetailView.as_view(), name="detail"),
]