from django.test import TestCase
from django.contrib.auth import get_user_model

from apps.blog.models import Post, Category, Tag


User = get_user_model()


class PostModelTest(TestCase):
    """Tests for Post model fields, defaults, and save() logic."""

    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="testpass123",
        )
        self.category = Category.objects.create(name="Django")
        self.tag = Tag.objects.create(name="Python")
        self.post = Post.objects.create(
            author=self.user,
            title="My First Post",
            content="Hello world",
            status=Post.Status.DRAFT,
        )

    def test_post_creation(self):
        """Post is created with correct fields and defaults."""
        self.assertEqual(self.post.title, "My First Post")
        self.assertEqual(self.post.author, self.user)
        self.assertEqual(self.post.view_count, 0)
        self.assertEqual(self.post.status, Post.Status.DRAFT)
        self.assertTrue(Post.objects.filter(pk=self.post.pk).exists())

    def test_str_method(self):
        """__str__ returns post title."""
        self.assertEqual(str(self.post), "My First Post")

    def test_slug_auto_generated(self):
        """Slug is auto-generated from title on first save."""
        self.assertEqual(self.post.slug, "my-first-post")

    def test_slug_unique_on_duplicate_title(self):
        """Duplicate title gets incremented slug."""
        post2 = Post.objects.create(
            author=self.user,
            title="My First Post",
            content="Different content",
            status=Post.Status.DRAFT,
        )
        self.assertEqual(post2.slug, "my-first-post-1")

    def test_published_date_set_on_publish(self):
        """published_date is set automatically when status becomes PUBLISHED."""
        self.assertIsNone(self.post.published_date)
        self.post.status = Post.Status.PUBLISHED
        self.post.save()
        self.assertIsNotNone(self.post.published_date)

    def test_published_date_not_overwritten(self):
        """published_date is never overwritten on subsequent saves."""
        self.post.status = Post.Status.PUBLISHED
        self.post.save()
        first_published = self.post.published_date

        self.post.title = "Updated Title"
        self.post.save()
        self.assertEqual(self.post.published_date, first_published)

    def test_timestamps_are_set(self):
        """created_date and updated_date are set automatically."""
        self.assertIsNotNone(self.post.created_date)
        self.assertIsNotNone(self.post.updated_date)

    def test_category_relationship(self):
        """Post can be assigned to multiple categories."""
        self.post.categories.add(self.category)
        self.assertIn(self.category, self.post.categories.all())