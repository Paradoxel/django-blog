from django.test import TestCase
from apps.accounts.models import User,Profile

class UserModelTest(TestCase):
    def test_get_full_name_returns_full_name(self):
        user = User.objects.create_user(
            email="test@example.com",
            password="123456789",
            first_name="Mohammadreza",
            last_name="Amini",
        )

        result = user.get_full_name()

        self.assertEqual(result, "Mohammadreza Amini")


    def test_get_full_name_returns_email_when_names_are_empty(self):
        user = User.objects.create_user(
            email="test@example.com",
            password="123456789",
            first_name="",
            last_name="",
        )
        result = user.get_full_name()
        self.assertEqual(result, "test@example.com")


class ProfileModelTest(TestCase):
    def test_profile_str_returns_user_full_name(self):
        user = User.objects.create_user(
            email="test@example.com",
            password="123456789",
            first_name="Ali",
            last_name="Amini",
        )
        # profile will create for single create User
        profile=Profile.objects.get(user=user)
        self.assertEqual(str(profile),"Ali Amini's profile")