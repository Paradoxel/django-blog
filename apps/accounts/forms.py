from django import forms
from django.contrib.auth import get_user_model
from apps.accounts.models import Profile
User = get_user_model()


class UserRegisterForm(forms.ModelForm):
    """
    User registration form.

    Handles:
    - Email-based registration
    - Password confirmation
    - Secure password hashing on save
    """

    password1 = forms.CharField(
        widget=forms.PasswordInput,
        label="Password",
        help_text="Enter a strong password"
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput,
        label="Confirm Password",
        help_text="Repeat the password for confirmation"
    )

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name"]

    def clean(self):
        """
        Validate that both passwords match before creating user.
        """
        cleaned_data = super().clean()

        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data

    def save(self, commit=True):
        """
        Create user instance with hashed password.
        """
        user = super().save(commit=False)

        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()

        return user
    


class UserUpdateForm(forms.ModelForm):
    """Form for updating User model fields."""
    class Meta:
        model = User
        fields = ['first_name','last_name']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "avatar",
            "bio",
            "phone_number",
            "website",
            "github",
            "twitter",
            "facebook",
            "linkedin",
        ]