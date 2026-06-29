from django import forms
from django.contrib.auth import get_user_model
from apps.accounts.models import Profile,WriterRequest
from django.contrib.auth.forms import PasswordChangeForm

User = get_user_model()


class UserRegisterForm(forms.ModelForm):
    """
    Minimal and clean registration form.

    Responsibility:
    - Create user with email
    - Validate password confirmation
    - Hash password securely
    """

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Enter your password",
                "class": "auth-input"
            }
        ),
        label="Password"
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Confirm your password",
                "class": "auth-input"
            }
        ),
        label="Confirm Password"
    )

    class Meta:
        model = User
        fields = ["email"]

        widgets = {
            "email": forms.EmailInput(
                attrs={
                    "placeholder": "Enter your email address",
                    "class": "auth-input"
                }
            )
        }

    def clean(self):
        cleaned_data = super().clean()

        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data

    def save(self, commit=True):
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


from django.contrib.auth.forms import PasswordChangeForm


class CustomPasswordChangeForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["old_password"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Current password",

        })

        self.fields["new_password1"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "New password",
        })

        self.fields["new_password2"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Confirm new password",
        })



class DeleteAccountForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
        )
    )
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_email(self):
        email=self.cleaned_data.get('email')
        if email.lower() !=self.user.email.lower():
            raise forms.ValidationError("Email does not match your account.")
        return email
        
    def clean_password(self):
        password=self.cleaned_data.get('password')
        if not self.user.check_password(password):
           raise forms.ValidationError(
                "Password is incorrect."
            )
        return password
    

class WriterRequestForm(forms.ModelForm):
    class Meta:
        model = WriterRequest
        fields = ["reason"]