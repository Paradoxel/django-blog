from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model

from apps.blog.models import Post


User = get_user_model()


class BlogListViewTest(TestCase):
    """Tests for blog post list view."""

    def setUp(self):
        self.url = reverse("blog:index")
        self.user = User.objects.create_user(
            email="test@gmail.com",
            password="1234",
        )
        self.image = SimpleUploadedFile(
            name="test.jpg",
            content=b"fake-image-content",
            content_type="image/jpeg",
        )
        self.post = Post.objects.create(
            author=self.user,
            title="Django Testing",
            content="Test Content",
            status=Post.Status.PUBLISHED,
            image=self.image,
        )

    def test_status_code(self):
        """List view returns 200."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        """List view uses correct template."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "blog/blog-home.html")

    def test_context_contains_posts(self):
        """Context includes posts queryset."""
        response = self.client.get(self.url)
        self.assertIn("posts", response.context)

    def test_post_title_rendered(self):
        """Published post title appears in response."""
        response = self.client.get(self.url)
        self.assertContains(response, "Django Testing")

    def test_draft_not_visible(self):
        """Draft posts are not shown in the list."""
        Post.objects.create(
            author=self.user,
            title="Hidden Draft",
            content="Secret",
            status=Post.Status.DRAFT,
            image=self.image,
        )
        response = self.client.get(self.url)
        self.assertNotContains(response, "Hidden Draft")