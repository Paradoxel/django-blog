from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView, CreateView

from apps.core.forms import ContactForm, NewsletterForm
from apps.core.models import Newsletter


class HomeView(TemplateView):
    """Render the home page."""

    template_name = "core/index.html"


class AboutView(TemplateView):
    """Render the about page."""

    template_name = "core/about.html"


class ContactView(FormView):
    """
    Handle contact form submission.
    Saves message to DB and shows success feedback.
    """

    template_name = "core/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("core:contact")

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Your message sent successfully!")
        return super().form_valid(form)


class NewsletterSubscribeView(CreateView):
    """
    Handle newsletter subscription.
    Redirects back to referring page after subscribe attempt.
    """

    model = Newsletter
    form_class = NewsletterForm

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "You have successfully subscribed!")
        return redirect(self.request.META.get("HTTP_REFERER", "/"))

    def form_invalid(self, form):
        email_errors = form.errors.get("email")
        if email_errors:
            messages.error(self.request, email_errors[0])
        else:
            messages.error(self.request, "Please enter a valid email address.")
        return redirect(self.request.META.get("HTTP_REFERER", "/"))