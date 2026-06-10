from django.test import TestCase
from django.db import IntegrityError

from apps.core.models import Contact, Newsletter


class ContactModelTest(TestCase):
    """Tests for Contact model fields and constraints."""

    def setUp(self):
        self.contact = Contact.objects.create(
            name="Mohammadreza",
            email="test@example.com",
            subject="Test Subject",
            message="Hello world",
        )

    def test_contact_creation(self):
        """Contact is saved to DB with correct fields."""
        self.assertEqual(self.contact.name, "Mohammadreza")
        self.assertEqual(self.contact.email, "test@example.com")
        self.assertTrue(Contact.objects.filter(pk=self.contact.pk).exists())

    def test_str_method(self):
        """__str__ returns name and subject."""
        self.assertEqual(str(self.contact), "Mohammadreza - Test Subject")

    def test_created_date_is_set(self):
        """created_date is set automatically on creation."""
        self.assertIsNotNone(self.contact.created_date)

    def test_missing_email_raises_error(self):
        """Creating contact without email raises IntegrityError."""
        with self.assertRaises(IntegrityError):
            Contact.objects.create(
                name="Ali",
                email=None,
                subject="Test",
                message="Hello",
            )

    def test_missing_name_raises_error(self):
        """Creating contact without name raises IntegrityError."""
        with self.assertRaises(IntegrityError):
            Contact.objects.create(
                name=None,
                email="test@example.com",
                subject="Test",
                message="Hello",
            )


class NewsletterModelTest(TestCase):
    """Tests for Newsletter model fields and constraints."""

    def setUp(self):
        self.newsletter = Newsletter.objects.create(email="test@gmail.com")

    def test_str_method(self):
        """__str__ returns email address."""
        self.assertEqual(str(self.newsletter), "test@gmail.com")

    def test_duplicate_email_raises_error(self):
        """Duplicate email raises IntegrityError — unique=True enforced."""
        with self.assertRaises(IntegrityError):
            Newsletter.objects.create(email="test@gmail.com")