from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView,UpdateView,TemplateView
from apps.accounts.forms import UserUpdateForm,ProfileUpdateForm
from apps.blog.models import Comment,Like,SavedPost
from .forms import UserRegisterForm
from apps.accounts.models import UserTypes
from itertools import chain
from django.views.generic import ListView
from apps.blog.models import Post
from apps.accounts.permissions import WriterRequiredMixin
User = get_user_model()


class UserLoginView(LoginView):
    """
    Handle user login using Django built-in authentication system.
    """

    template_name = "accounts/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        """
        Redirect user after successful login.
        """
        return reverse_lazy("core:home")


class UserRegisterView(CreateView):
    """
    Handle user registration using custom user model.
    """

    model = User
    form_class = UserRegisterForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("accounts:login")


@login_required
def user_logout(request):
    """
    Log out the current user and redirect to home page.
    """
    if(request.method=='POST'):
        logout(request)
        messages.success(request, "You have been logged out successfully.")
    return redirect("core:home")




# for update the user profile 
class UpdateUserProfile(LoginRequiredMixin,UpdateView):
    """
    Handle profile update for logged-in users.
    Updates both User and Profile models in one submission.
    """
    template_name = "accounts/profile.html"
    form_class=UserUpdateForm
    def get_success_url(self):
        return reverse_lazy("accounts:profile")
    def get_object(self, queryset = ...):
        # return current user
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method=='POST':
            context['profile_form']= ProfileUpdateForm(
                self.request.POST,
                self.request.FILES, # needed for avatar
                instance=self.get_object().profile,
            )
        else:
            context["profile_form"] = ProfileUpdateForm(
                    instance=self.get_object().profile
            )
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        profile_form = context["profile_form"]

        if form.is_valid() and profile_form.is_valid():
            self.object = form.save()
            profile_form.save()

            messages.success(self.request, "Profile updated successfully")

            return redirect(self.get_success_url())

        return self.form_invalid(form)
        
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
    


class UserEngagementView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/engagement.html"

    def get_activity_type(self):
        # default should be ALL
        return self.request.GET.get("activity_type", "all")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        activity_type = self.get_activity_type()

        context["activity_type"] = activity_type

        activities = []

        # --------------------
        # COMMENTS
        # --------------------
        if activity_type == "comments":
            activities = Comment.objects.filter(user=user).select_related("post")
            for a in activities:
                a.activity_type = "comment"

        # --------------------
        # LIKES
        # --------------------
        elif activity_type == "likes":
            activities = Like.objects.filter(user=user).select_related("post")
            for a in activities:
                a.activity_type = "like"

        # --------------------
        # SAVED
        # --------------------
        elif activity_type == "saved":
            activities = SavedPost.objects.filter(user=user).select_related("post")
            for a in activities:
                a.activity_type = "saved"

        # --------------------
        # ALL (DEFAULT)
        # --------------------
        else:
            comments = Comment.objects.filter(user=user).select_related("post")
            likes = Like.objects.filter(user=user).select_related("post")
            saved = SavedPost.objects.filter(user=user).select_related("post")

            activities = sorted(
                list(comments) + list(likes) + list(saved),
                key=lambda x: x.created_date,
                reverse=True
            )

            for a in activities:
                if isinstance(a, Comment):
                    a.activity_type = "comment"
                elif isinstance(a, Like):
                    a.activity_type = "like"
                elif isinstance(a, SavedPost):
                    a.activity_type = "saved"

        # writer check
        context["is_writer"] = self.request.user.profile.user_type == UserTypes.WRITER

        context["activities"] = activities

        return context
    


class MyPostsView(LoginRequiredMixin,WriterRequiredMixin,ListView):
    model=Post
    template_name='accounts/my_posts.html'
    context_object_name='posts'
    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)
    