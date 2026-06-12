from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model

from apps.blog.models import Post, Comment


User = get_user_model()


def make_image():
    """Return a minimal fake image for post creation."""
    return SimpleUploadedFile(
        name="test.jpg",
        content=b"fake-image-content",
        content_type="image/jpeg",
    )


class CommentModelTest(TestCase):
    """Tests for Comment model, QuerySet filters, and DB constraints."""

    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="testpass123",
        )
        self.post = Post.objects.create(
            author=self.user,
            title="Test Post",
            content="Test Content",
            status=Post.Status.PUBLISHED,
            image=make_image(),
        )
        self.comment = Comment.objects.create(
            post=self.post,
            name="Ali",
            email="ali@example.com",
            message="Great post!",
        )

    def test_creation(self):
        """Comment saved with correct fields and pending by default."""
        self.assertEqual(self.comment.name, "Ali")
        self.assertFalse(self.comment.is_approved)
        self.assertTrue(Comment.objects.filter(pk=self.comment.pk).exists())

    def test_str_method(self):
        """__str__ returns name and post title."""
        self.assertEqual(str(self.comment), "Ali → Test Post")

    def test_approved_queryset(self):
        """approved() returns only approved comments."""
        Comment.objects.create(post=self.post, name="Bob", message="Nice!", is_approved=True)
        self.assertEqual(Comment.objects.approved().count(), 1)

    def test_pending_queryset(self):
        """pending() returns only unapproved comments."""
        self.assertEqual(Comment.objects.pending().count(), 1)

    def test_deleted_with_post(self):
        """Comment is deleted when post is deleted — CASCADE."""
        self.post.delete()
        self.assertFalse(Comment.objects.filter(pk=self.comment.pk).exists())

    def test_user_set_null_on_delete(self):
        """Comment user becomes None when user is deleted — SET_NULL."""
        commenter = User.objects.create_user(email="c@example.com", password="pass")
        comment = Comment.objects.create(post=self.post, user=commenter, name="X", message="Hi!")
        commenter.delete()
        comment.refresh_from_db()
        self.assertIsNone(comment.user)


class CommentSubmissionTest(TestCase):
    """Tests for comment form submission via POST request."""

    def setUp(self):
        user = User.objects.create_user(email="test@example.com", password="testpass123")
        self.post = Post.objects.create(
            author=user,
            title="Test Post",
            content="Content",
            status=Post.Status.PUBLISHED,
            image=make_image(),
        )
        self.url = reverse("blog:detail", args=[self.post.slug])
        self.valid_data = {"name": "Ali", "email": "ali@example.com", "message": "Great post!"}

    def test_valid_comment_saved(self):
        """Valid comment is saved to DB."""
        self.client.post(self.url, self.valid_data)
        self.assertEqual(Comment.objects.count(), 1)

    def test_comment_pending_by_default(self):
        """Submitted comment requires admin approval."""
        self.client.post(self.url, self.valid_data)
        self.assertFalse(Comment.objects.first().is_approved)

    def test_invalid_comment_not_saved(self):
        """Empty message does not create a comment."""
        self.client.post(self.url, {**self.valid_data, "message": ""})
        self.assertEqual(Comment.objects.count(), 0)

    def test_valid_comment_redirects(self):
        """Valid submission redirects back to post."""
        response = self.client.post(self.url, self.valid_data)
        self.assertRedirects(response, self.url)

    def test_only_approved_comments_visible(self):
        """Context only contains approved comments."""
        Comment.objects.create(post=self.post, name="Ali", message="Approved!", is_approved=True)
        Comment.objects.create(post=self.post, name="Bob", message="Pending...", is_approved=False)
        comments = self.client.get(self.url).context["comments"]
        self.assertEqual(comments.count(), 1)
        self.assertEqual(comments.first().name, "Ali")