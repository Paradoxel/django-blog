from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from apps.blog.models import Post, Category
from apps.accounts.models import User


# =========================
# BLOG LIST VIEW TESTS
# =========================
class BlogListViewTest(TestCase):

    def setUp(self):
        self.url = reverse("blog:index")

        self.user = User.objects.create_user(
            email="test@gmail.com",
            password="1234"
        )

        self.image = SimpleUploadedFile(
            name="test.jpg",
            content=b"fake-image-content",
            content_type="image/jpeg"
        )

        self.post = Post.objects.create(
            author=self.user,
            title="Django Testing",
            content="Test Content",
            status=Post.Status.PUBLISHED,
            image=self.image,
        )

    def test_status_code_is_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_correct_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "blog/blog-home.html")

    def test_context_contains_posts(self):
        response = self.client.get(self.url)
        self.assertIn("posts", response.context)

    def test_posts_are_rendered(self):
        response = self.client.get(self.url)
        self.assertContains(response, "Django Testing")


# =========================
# BLOG CATEGORY TESTS
# =========================
class BlogCategoryTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="test@gmail.com",
            password="1234"
        )

        self.category = Category.objects.create(
            name="Django"
        )

        self.image = SimpleUploadedFile(
            name="test.jpg",
            content=b"fake-image-content",
            content_type="image/jpeg"
        )

        self.post = Post.objects.create(
            author=self.user,
            title="Test Post",
            content="Test Content",
            status=Post.Status.PUBLISHED,
            image=self.image,
        )

        self.post.categories.add(self.category)

    def test_post_has_category(self):
        self.assertIn(self.category, self.post.categories.all())