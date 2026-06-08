from django.shortcuts import redirect
from django.views.generic import TemplateView,FormView,CreateView
from apps.core.forms import ContactForm,NewsletterForm
from apps.core.models import Newsletter
from django.urls import reverse_lazy
from django.contrib import messages
class HomeView(TemplateView):
    template_name = "core/index.html"


class AboutView(TemplateView):
    template_name = "core/about.html"


class ContactView(FormView):
    template_name = 'core/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('core:contact')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Your message sent successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Something went wrong. Please check the form.")
        return super().form_invalid(form)


class NewsletterSubscribeView(CreateView):
    model = Newsletter
    form_class = NewsletterForm

    def form_valid(self, form):
        form.save()

        messages.success(
            self.request,
            "You have successfully subscribed to our newsletter."
        )

        return redirect(
            self.request.META.get("HTTP_REFERER", "/")
        )

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Please enter a valid email address."
        )

        return redirect(
            self.request.META.get("HTTP_REFERER", "/")
        )
