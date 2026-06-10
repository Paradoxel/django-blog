from django.test import TestCase

from apps.accounts.models import User, Profile


class UserModelTest(TestCase):
    """Tests for custom User model methods."""

    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="123456789",
            first_name="Mohammadreza",
            last_name="Amini",
        )

    def test_get_full_name_returns_full_name(self):
        """get_full_name returns first and last name combined."""
        self.assertEqual(self.user.get_full_name(), "Mohammadreza Amini")

    def test_get_full_name_returns_email_when_names_are_empty(self):
        """get_full_name falls back to email when names are empty."""
        user = User.objects.create_user(
            email="nname@example.com",
            password="123456789",
        )
        self.assertEqual(user.get_full_name(), "nname@example.com")


class ProfileModelTest(TestCase):
    """Tests for Profile model and signal-based auto-creation."""

    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="123456789",
            first_name="Ali",
            last_name="Amini",
        )

    def test_profile_auto_created_on_user_creation(self):
        """Profile is automatically created via signal when User is created."""
        self.assertTrue(Profile.objects.filter(user=self.user).exists())

    def test_str_method(self):
        """__str__ returns user full name with profile suffix."""
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(str(profile), "Ali Amini's profile")