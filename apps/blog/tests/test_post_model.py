from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.blog.models import Post, Category, Tag

User = get_user_model()


class PostModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="testpass123"
        )

        self.category = Category.objects.create(
            name="Django"
        )

        self.tag = Tag.objects.create(
            name="Python"
        )

    # -----------------------------------
    # 1. BASIC CREATION TEST
    # -----------------------------------
    def test_post_creation(self):
        post = Post.objects.create(
            author=self.user,
            title="My First Post",
            content="Hello world",
            status=True,
        )

        post.categories.add(self.category)

        self.assertEqual(post.title, "My First Post")
        self.assertEqual(post.author, self.user)
        self.assertTrue(Post.objects.filter(pk=post.pk).exists())
        self.assertIn(self.category, post.categories.all())

    # -----------------------------------
    # 2. STRING REPRESENTATION
    # -----------------------------------
    def test_post_str_method(self):
        post = Post.objects.create(
            author=self.user,
            title="My First Post",
            content="Hello world",
            status=True,
        )

        self.assertEqual(str(post), "My First Post")

    # -----------------------------------
    # 3. DEFAULT VALUES TEST
    # -----------------------------------
    def test_post_default_values(self):
        post = Post.objects.create(
            author=self.user,
            title="Post Title",
            content="Post Content",
            status=True,
        )

        # adjust this if your model has view_count
        if hasattr(post, "view_count"):
            self.assertEqual(post.view_count, 0)

    # -----------------------------------
    # 4. TIMESTAMP TEST
    # -----------------------------------
    def test_post_created_date_is_set(self):
        post = Post.objects.create(
            author=self.user,
            title="Post Title",
            content="Post Content",
            status='published',
        )

        self.assertIsNotNone(post.created_date)

        # only if your model has updated_date
        if hasattr(post, "updated_date"):
            self.assertIsNotNone(post.updated_date)

    # -----------------------------------
    # 5. CATEGORY RELATIONSHIP TEST
    # -----------------------------------
    def test_post_category_relationship(self):
        post = Post.objects.create(
            author=self.user,
            title="Post Title",
            content="Post Content",
            status=True,
        )

        post.categories.add(self.category)

        self.assertIn(self.category, post.categories.all())