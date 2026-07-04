from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("register/", views.UserRegisterView.as_view(), name="register"),
    path("logout/", views.user_logout, name="logout"),

    path("profile/", views.UpdateUserProfile.as_view(), name="profile"),
    path("engagement/", views.UserEngagementView.as_view(), name="engagement"),
    path("my_posts/", views.MyPostsView.as_view(), name="my_posts"),

    path("posts/create/", views.CreatePostView.as_view(), name="post_create"),
    path("posts/<slug:slug>/edit/", views.PostUpdateView.as_view(), name="post_edit"),
    path("posts/<slug:slug>/delete/", views.PostDeleteView.as_view(), name="post_delete"),

    path("security/", views.UserSecurityView.as_view(), name="security"),
    path(
        "security/password/",
        views.UserPasswordChangeView.as_view(),
        name="security_password",
    ),
    path(
        "security/sessions/",
        views.UserSessionsView.as_view(),
        name="security_sessions",
    ),
    path(
        "security/sessions/logout/<str:session_key>/",
        views.LogoutSessionView.as_view(),
        name="logout_session",
    ),
    path(
        "security/sessions/logout-other/",
        views.LogoutOtherSessionsView.as_view(),
        name="logout_other_sessions",
    ),

    path(
        "security/delete-account/",
        views.DeleteAccountView.as_view(),
        name="delete_account",
    ),
    path(
        "security/delete-account/confirm/",
        views.DeleteAccountConfirmView.as_view(),
        name="delete_account_confirm",
    ),

    path(
        "become-writer/",
        views.BecomeWriterView.as_view(),
        name="become_writer",
    ),
]