from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import UserRegisterForm


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
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("core:home")