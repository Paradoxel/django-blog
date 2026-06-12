from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    """Form for submitting blog comments."""

    class Meta:
        model = Comment
        fields = ("name", "email", "subject", "message")

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
            "subject": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Subject",
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