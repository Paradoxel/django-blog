from django.test import TestCase
from apps.accounts.models import User

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