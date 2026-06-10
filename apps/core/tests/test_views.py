from django.test import TestCase
from django.urls import reverse

from apps.core.models import Newsletter


class HomeViewTest(TestCase):
    """Tests for home page view."""

    def setUp(self):
        self.url = reverse("core:home")

    def test_status_code(self):
        """Home page returns 200."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        """Home page uses correct template."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "core/index.html")

    def test_contains_expected_text(self):
        """Home page contains Travel text."""
        response = self.client.get(self.url)
        self.assertContains(response, "Travel")


class AboutViewTest(TestCase):
    """Tests for about page view."""

    def setUp(self):
        self.url = reverse("core:about")

    def test_status_code(self):
        """About page returns 200."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        """About page uses correct template."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "core/about.html")

    def test_contains_expected_text(self):
        """About page contains About Us text."""
        response = self.client.get(self.url)
        self.assertContains(response, "About Us")


class ContactViewTest(TestCase):
    """Tests for contact page view."""

    def setUp(self):
        self.url = reverse("core:contact")

    def test_status_code(self):
        """Contact page returns 200."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        """Contact page uses correct template."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "core/contact.html")

    def test_contains_expected_text(self):
        """Contact page contains Contact Us text."""
        response = self.client.get(self.url)
        self.assertContains(response, "Contact Us")


class NewsletterViewTest(TestCase):
    """Tests for newsletter subscription view."""

    def setUp(self):
        self.url = reverse("core:newsletter_subscribe")

    def test_can_subscribe(self):
        """Valid email creates newsletter subscription."""
        self.client.post(self.url, {"email": "test@gmail.com"})
        self.assertEqual(Newsletter.objects.count(), 1)

    def test_duplicate_email_not_subscribed(self):
        """Duplicate email does not create second subscription."""
        self.client.post(self.url, {"email": "test@gmail.com"})
        self.client.post(self.url, {"email": "test@gmail.com"})
        self.assertEqual(Newsletter.objects.count(), 1)