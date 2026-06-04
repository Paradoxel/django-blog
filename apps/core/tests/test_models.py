from django.test import TestCase
from django.db import IntegrityError
from apps.core.models import Contact


class ContactModelTest(TestCase):

    # -----------------------------
    # VALID DATA TESTS
    # -----------------------------

    def test_contact_creation_with_valid_data(self):
        contact = Contact.objects.create(
            name="Mohammadreza",
            email="a1mmdrez@gmail.com",
            subject="This is test subject",
            message="Hello world"
        )

        self.assertEqual(contact.name, "Mohammadreza")
        self.assertEqual(contact.email, "a1mmdrez@gmail.com")
        self.assertTrue(Contact.objects.filter(pk=contact.pk).exists())

    def test_contact_str_method(self):
        contact = Contact.objects.create(
            name="Mohammadreza",
            email="test@example.com",
            subject="This is test subject",
            message="Hello world"
        )

        self.assertEqual(str(contact), "Mohammadreza - This is test subject")

    def test_contact_created_date_is_set(self):
        contact = Contact.objects.create(
            name="Ali",
            email="ali@example.com",
            subject="Test",
            message="Hello"
        )

        self.assertIsNotNone(contact.created_date)

    # -----------------------------
    # INVALID DATA TESTS
    # -----------------------------

    def test_contact_missing_email_should_raise_error(self):
        with self.assertRaises(IntegrityError):
            Contact.objects.create(
                name="Ali",
                email=None,
                subject="Test",
                message="Hello"
            )

    def test_contact_missing_name_should_raise_error(self):
        with self.assertRaises(IntegrityError):
            Contact.objects.create(
                name=None,
                email="test@example.com",
                subject="Test",
                message="Hello"
            )