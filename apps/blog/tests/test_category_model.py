from django.test import TestCase

from apps.blog.models import Category


class CategoryModelTest(TestCase):
    """Tests for Category model fields and save() logic."""

    def setUp(self):
        self.category = Category.objects.create(name="Django Tutorials")

    def test_category_creation(self):
        """Category is saved to DB with correct name."""
        self.assertEqual(self.category.name, "Django Tutorials")
        self.assertTrue(Category.objects.filter(pk=self.category.pk).exists())

    def test_slug_auto_generated(self):
        """Slug is auto-generated from name on first save."""
        self.assertEqual(self.category.slug, "django-tutorials")

    def test_str_method(self):
        """__str__ returns category name."""
        self.assertEqual(str(self.category), "Django Tutorials")