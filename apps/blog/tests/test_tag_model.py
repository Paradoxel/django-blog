from django.test import TestCase

from apps.blog.models import Tag


class TagModelTest(TestCase):
    """Tests for Tag model fields and save() logic."""

    def setUp(self):
        self.tag = Tag.objects.create(name="Python Django")

    def test_tag_creation(self):
        """Tag is saved to DB with correct name."""
        self.assertEqual(self.tag.name, "Python Django")
        self.assertTrue(Tag.objects.filter(pk=self.tag.pk).exists())

    def test_slug_auto_generated(self):
        """Slug is auto-generated from name on first save."""
        self.assertEqual(self.tag.slug, "python-django")

    def test_str_method(self):
        """__str__ returns tag name."""
        self.assertEqual(str(self.tag), "Python Django")