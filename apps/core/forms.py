from django import forms
from captcha.fields import CaptchaField
from apps.core.models import Contact,Newsletter


class ContactForm(forms.ModelForm):

    captcha = CaptchaField(
        error_messages={
            "invalid": "Incorrect captcha code. Please try again."
        }
    )

    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if len(name) < 2:
            raise forms.ValidationError("Name is too short")
        return name

    def clean_message(self):
        message = self.cleaned_data.get("message")
        if len(message) < 10:
            raise forms.ValidationError("Message is too short")
        return message


class NewsletterForm(forms.ModelForm):
    class Meta:
        model=Newsletter
        fields =['email']

    def clean_email(self):
        email = self.cleaned_data["email"]

        if Newsletter.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "You are already subscribed to our newsletter."
            )

        return email