from django.urls import path

from .views import (UserLoginView,
                    UserRegisterView,
                    user_logout,
                    UpdateUserProfile,
                    UserEngagementView,
                    MyPostsView,
                    CreatePostView)

app_name = "accounts"

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("logout/", user_logout , name="logout"),
    path('profile/',UpdateUserProfile.as_view(),name='profile'),
    path('engagement/',UserEngagementView.as_view(),name='engagement'),
    path('my_posts/',MyPostsView.as_view(),name='my_posts'),
    path("posts/create/", CreatePostView.as_view(), name="post_create"),
]