from django.test import TestCase
from apps.blog.models import Tag


class TagModelTest(TestCase):

    def test_tag_creation_and_slug(self):
        tag = Tag.objects.create(
            name="Python Django"
        )

        self.assertEqual(tag.name, "Python Django")
        self.assertEqual(tag.slug, "python-django")

        self.assertTrue(
            Tag.objects.filter(pk=tag.pk).exists()
        )

    def test_tag_str_method(self):
        tag = Tag.objects.create(
            name="Python Django"
        )

        self.assertEqual(str(tag), "Python Django")