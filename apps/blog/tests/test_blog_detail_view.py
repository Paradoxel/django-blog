from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model

from apps.blog.models import Post


User = get_user_model()


class BlogDetailViewTest(TestCase):
    """Tests for blog post detail view."""

    def setUp(self):
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
            title="Detail View Post",
            content="This is a test post for detail view",
            status=Post.Status.PUBLISHED,
            image=self.image,
        )
        self.url = reverse("blog:detail", args=[self.post.slug])

    def test_status_code(self):
        """Detail view returns 200 for published post."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        """Detail view uses correct template."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "blog/blog-single.html")

    def test_context_contains_post(self):
        """Context includes the post object."""
        response = self.client.get(self.url)
        self.assertIn("post", response.context)

    def test_correct_post_returned(self):
        """Context contains the correct post."""
        response = self.client.get(self.url)
        self.assertEqual(response.context["post"], self.post)

    def test_post_title_rendered(self):
        """Post title appears in response."""
        response = self.client.get(self.url)
        self.assertContains(response, "Detail View Post")

    def test_invalid_slug_returns_404(self):
        """Non-existent slug returns 404."""
        url = reverse("blog:detail", args=["wrong-slug"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_draft_returns_404(self):
        """Draft post is not accessible — returns 404."""
        draft = Post.objects.create(
            author=self.user,
            title="Draft Post",
            content="Secret content",
            status=Post.Status.DRAFT,
            image=self.image,
        )
        url = reverse("blog:detail", args=[draft.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)