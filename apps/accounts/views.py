from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.db import transaction
from django.views.generic import CreateView,UpdateView,TemplateView
from apps.accounts.forms import UserUpdateForm,ProfileUpdateForm,DeleteAccountForm
from apps.blog.models import Comment,Like,SavedPost
from .forms import UserRegisterForm
from apps.accounts.models import UserTypes
from itertools import chain
from django.views.generic import ListView,DeleteView
from apps.blog.models import Post
from apps.accounts.permissions import WriterRequiredMixin,DeleteAccountVerificationRequiredMixin
from apps.blog.forms import PostForm
from django.contrib.auth.views import PasswordChangeView
from apps.accounts.forms import CustomPasswordChangeForm
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.views.generic import TemplateView,FormView
from django.views.generic import View
from django.shortcuts import get_object_or_404
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
    


class UserEngagementView(LoginRequiredMixin, ListView):
    template_name = "accounts/engagement.html"
    paginate_by = 3
    context_object_name = "activities"

    def get_queryset(self):
        user = self.request.user
        activity_type = self.request.GET.get("activity_type", "all")

        if activity_type == "comments":
            return Comment.objects.filter(user=user).select_related("post")

        elif activity_type == "likes":
            return Like.objects.filter(user=user).select_related("post")

        elif activity_type == "saved":
            return SavedPost.objects.filter(user=user).select_related("post")

        else:
            comments = Comment.objects.filter(user=user).select_related("post")
            likes = Like.objects.filter(user=user).select_related("post")
            saved = SavedPost.objects.filter(user=user).select_related("post")

            activities = list(chain(comments, likes, saved))
            activities.sort(key=lambda x: x.created_date, reverse=True)

            return activities


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        activity_type = self.request.GET.get("activity_type", "all")

        context["activity_type"] = activity_type

        context["comments_count"] = Comment.objects.filter(user=user).count()
        context["likes_count"] = Like.objects.filter(user=user).count()
        context["saved_count"] = SavedPost.objects.filter(user=user).count()

        context["total_activity"] = (
            context["comments_count"]
            + context["likes_count"]
            + context["saved_count"]
        )

        context["is_writer"] = (
            user.profile.user_type == UserTypes.WRITER
        )

        return context

class MyPostsView(LoginRequiredMixin,WriterRequiredMixin,ListView):
    model=Post
    template_name='accounts/my_posts.html'
    context_object_name='posts'
    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)
    

class CreatePostView(LoginRequiredMixin,WriterRequiredMixin,CreateView):
    model = Post
    form_class = PostForm
    template_name = "accounts/post_form.html"
    success_url = reverse_lazy("accounts:my_posts")
    def form_valid(self, form):
        # STEP 1: attach author automatically (security)
        form.instance.author = self.request.user

        # STEP 2: force CMS workflow state
        form.instance.status = Post.Status.DRAFT

        # STEP 3: save normally
        return super().form_valid(form)
    


class PostUpdateView(LoginRequiredMixin,WriterRequiredMixin,UpdateView):
    model=Post
    form_class=PostForm
    template_name='accounts/post_form.html'
    success_url = reverse_lazy("accounts:my_posts")
    slug_field = "slug"
    def form_valid(self, form):
        form.instance.status=Post.Status.DRAFT
        return super().form_valid(form)
    

class PostDeleteView(LoginRequiredMixin,WriterRequiredMixin,DeleteView):
    model=Post
    template_name = "accounts/post_confirm_delete.html"
    success_url = reverse_lazy("accounts:my_posts")
    slug_field='slug'
    slug_url_kwarg='slug'
    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)
    


class UserSecurityView(LoginRequiredMixin,TemplateView):
    template_name='accounts/security/security.html'



class UserPasswordChangeView(LoginRequiredMixin,PasswordChangeView):
    template_name = "accounts/security/security_password.html"
    success_url = reverse_lazy("accounts:security")
    form_class = CustomPasswordChangeForm
    def form_valid(self, form):
        messages.success(
            self.request,
            "Password updated successfully."
        )
        return super().form_valid(form)
    


class UserSessionsView(LoginRequiredMixin, ListView):
    model = Session
    template_name = "accounts/security/security_sessions.html"
    context_object_name = "sessions"
    paginate_by = 3

    def get_queryset(self):
        queryset = Session.objects.filter(
            expire_date__gte=timezone.now()
        )

        result = []

        for session in queryset:
            data = session.get_decoded()

            if data.get("_auth_user_id") == str(self.request.user.pk):
                result.append({
                    "session_key": session.session_key,
                    "expire_date": session.expire_date,
                    "is_current": (
                        session.session_key ==
                        self.request.session.session_key
                    ),
                })

        return result



class LogoutSessionView(LoginRequiredMixin, View):

    def post(self, request, session_key, *args, **kwargs):

        session = get_object_or_404(
            Session.objects.filter(expire_date__gte=timezone.now()),
            session_key=session_key,
        )

        data = session.get_decoded()

        if data.get("_auth_user_id") != str(request.user.pk):
            messages.error(request, "Invalid session.")
            return redirect("accounts:security_sessions")

        session.delete()

        messages.success(
            request,
            "Session signed out successfully.",
        )

        return redirect("accounts:security_sessions")

class LogoutOtherSessionsView(LoginRequiredMixin,View):
    def post(self,request,*args,**kwargs):
        current_session_key = request.session.session_key
        sessions=Session.objects.filter(expire_date__gte=timezone.now())
        for session in sessions:
            data = session.get_decoded()
            if data.get("_auth_user_id") == str(request.user.id):
                    if session.session_key != current_session_key:
                        session.delete()
        messages.success(
            request,
            "All other sessions have been signed out."
        )
        return redirect("accounts:security_sessions")
    



class DeleteAccountView(LoginRequiredMixin,FormView):
    template_name = "accounts/security/delete_account.html"
    form_class = DeleteAccountForm
    success_url = reverse_lazy("accounts:delete_account_confirm")
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user']=self.request.user
        return kwargs
    
    
    def form_valid(self, form):
        self.request.session["delete_account_verified"] = True
        return super().form_valid(form)
    



class DeleteAccountConfirmView(LoginRequiredMixin,DeleteAccountVerificationRequiredMixin,TemplateView):
    template_name = "accounts/security/delete_account_confirm.html"
    success_url = reverse_lazy('core:home')
    def post(self, request, *args, **kwargs):

        with transaction.atomic():

            user = request.user

            request.session.pop("delete_account_verified", None)

            logout(request)

            user.delete()

            messages.success(
                request,
                "Your account has been permanently deleted."
            )

        return redirect(self.success_url)
    


class BecomeWriterView()