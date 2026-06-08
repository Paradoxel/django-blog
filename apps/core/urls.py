from django.urls import path
from . import views

app_name = "core"
urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("contact/", views.ContactView.as_view(), name="contact"),
    path(
        "newsletter/subscribe/",
        views.NewsletterSubscribeView.as_view(),
        name="newsletter_subscribe",
    ),
]
