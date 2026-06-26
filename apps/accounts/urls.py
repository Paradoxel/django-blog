from django.urls import path

from .views import (UserLoginView,
                    UserRegisterView,
                    user_logout,
                    UpdateUserProfile,
                    UserEngagementView,
                    MyPostsView,
                    CreatePostView,
                    PostUpdateView,
                    PostDeleteView,
                    UserSecurityView,
                    UserPasswordChangeView,
                    UserSessionsView,
                    LogoutSessionView)

app_name = "accounts"

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("logout/", user_logout , name="logout"),
    path('profile/',UpdateUserProfile.as_view(),name='profile'),
    path('engagement/',UserEngagementView.as_view(),name='engagement'),
    path('my_posts/',MyPostsView.as_view(),name='my_posts'),
    path("posts/create/", CreatePostView.as_view(), name="post_create"),
    path("posts/<slug:slug>/edit/", PostUpdateView.as_view(), name="post_edit"),
    path('posts/<slug:slug>/delete/',PostDeleteView.as_view(),name='post_delete'),
    path('security/',UserSecurityView.as_view(),name='security'),
    path('security/password/',UserPasswordChangeView.as_view(),name='security_password'),
    path('security/sessions/',UserSessionsView.as_view(),name='security_sessions'),
    path('security/sessions/logout/<str:session_key>/',LogoutSessionView.as_view(),name='logout_session'),
    #path('security/sessions/logout-others/',LogoutOtherSessionsView.as_view(),name="logout_other_sessions"),


]