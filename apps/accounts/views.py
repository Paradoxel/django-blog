from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth import get_user_model
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
    Handle user registration.
    """

    model = User
    form_class = UserRegisterForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("accounts:login")


class UserLogoutView(LogoutView):
    """
    Handle user Log out.
    """
    next_page=reverse_lazy('core:home')