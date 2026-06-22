from django import forms
from captcha.fields import CaptchaField
from .models import Comment,Post


class CommentForm(forms.ModelForm):
    """Form for submitting blog comments."""

    class Meta:
        model = Comment
        fields = ("name", "email", "message")

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter Name",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter email address",
                }
            ),
            "message": forms.Textarea(
                attrs={
                    "class": "form-control mb-10",
                    "rows": 5,
                    "placeholder": "Message",
                }
            ),
        }



class PostForm(forms.ModelForm):
    captcha = CaptchaField(
        error_messages={
            "invalid": "Incorrect captcha code. Please try again."
        }
    )
    class Meta:
        model=Post
        fields = [
            "title",
            "content",
            "excerpt",
            "image",
            "primary_tag",
            "categories",
        ]