from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from apps.blog.models import Post, Category
from apps.accounts.models import User


# =====================================================
# BLOG LIST VIEW TESTS
# =====================================================
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

    # status check
    def test_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    # template check
    def test_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "blog/blog-home.html")

    # context check
    def test_context_contains_posts(self):
        response = self.client.get(self.url)
        self.assertIn("posts", response.context)

    # content rendering
    def test_post_title_rendered(self):
        response = self.client.get(self.url)
        self.assertContains(response, "Django Testing")


# =====================================================
# BLOG CATEGORY TESTS
# =====================================================
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

    # relation check
    def test_post_category_relation(self):
        self.assertIn(self.category, self.post.categories.all())


# =====================================================
# BLOG DETAIL VIEW TESTS
# =====================================================
class BlogDetailViewTest(TestCase):

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
            title="Detail View Post",
            content="This is a test post for detail view",
            status=Post.Status.PUBLISHED,
            image=self.image,
        )

        self.post.categories.add(self.category)

        self.url = reverse("blog:detail", args=[self.post.slug])

    # status code
    def test_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    # template used
    def test_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "blog/blog-single.html")

    # post exists in context
    def test_context_contains_post(self):
        response = self.client.get(self.url)
        self.assertIn("post", response.context)

    # correct post returned
    def test_correct_post_returned(self):
        response = self.client.get(self.url)
        self.assertEqual(response.context["post"], self.post)

    # title rendered
    def test_post_title_rendered(self):
        response = self.client.get(self.url)
        self.assertContains(response, "Detail View Post")

    # 404 for invalid slug
    def test_invalid_slug_returns_404(self):
        url = reverse("blog:detail", args=["wrong-slug"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)