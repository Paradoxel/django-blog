from django.test import TestCase
from apps.blog.models import Category

class CategoryModelTest(TestCase):

    def test_category_creation_and_slug(self):
        category = Category.objects.create(
            name="Django Tutorials"
        )

        self.assertEqual(category.name, "Django Tutorials")
        self.assertTrue(category.slug)  # slug should exist
        self.assertEqual(category.slug, "django-tutorials")
        self.assertTrue(Category.objects.filter(pk=category.pk).exists)

    def test_category_str_method(self):
        category = Category.objects.create(
            name="Django Tutorials"
        )

        self.assertEqual(str(category), "Django Tutorials")