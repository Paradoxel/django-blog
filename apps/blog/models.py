from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse


class Tag(models.Model):
    """Content tag for labeling posts."""

    name = models.CharField(
        max_length=100,
        unique=True,
    )

    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True,
    )

    class Meta:
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Category(models.Model):
    """
    Organize posts into categories.
    """

    name = models.CharField(
        max_length=100,
        unique=True,
    )

    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True,
    )

    description = models.TextField(
        blank=True,
    )

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class PostQuerySet(models.QuerySet):
    """
    Semantic query interface for Post.
    Keeps filter logic in one place — views stay clean.
    """

    def published(self):
        return self.filter(status=Post.Status.PUBLISHED)

    def drafts(self):
        return self.filter(status=Post.Status.DRAFT)

    def archived(self):
        return self.filter(status=Post.Status.ARCHIVED)


class Post(models.Model):
    """
    Core blog post model.

    Handles the draft → published → archived workflow.
    Automatically generates a unique slug and sets the
    publication date on first publish.
    """

    class Status(models.TextChoices):
        """Publication lifecycle states."""

        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"
        ARCHIVED = "archived", "Archived"

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts",
    )

    title = models.CharField(max_length=255)

    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True,
    )

    excerpt = models.CharField(
        max_length=300,
        blank=True,
    )

    content = models.TextField()

    image = models.ImageField(
        upload_to="posts/%Y/%m/",
    )

    primary_tag = models.ForeignKey(
        Tag,
        on_delete=models.SET_NULL,
        related_name="primary_posts",
        null=True,
        blank=True,
    )

    categories = models.ManyToManyField(
        Category,
        related_name="posts",
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
        db_index=True,
    )

    view_count = models.PositiveIntegerField(default=0)

    published_date = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True,
    )

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    objects = PostQuerySet.as_manager()

    class Meta:
        ordering = ["-created_date"]

    def save(self, *args, **kwargs):
        """Generate a unique slug and set the publication date."""

        if not self.slug:
            base_slug = slugify(self.title[:240])
            slug = base_slug
            counter = 1

            while self.__class__.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        if (
            self.status == self.Status.PUBLISHED
            and not self.published_date
        ):
            self.published_date = timezone.now()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            "blog:detail",
            kwargs={"slug": self.slug},
        )

    @property
    def reading_time(self):
        """Estimate reading time (200 words per minute)."""
        word_count = len(self.content.split())
        return max(1, round(word_count / 200))

    @property
    def status_label(self):
        """Return a human-friendly status label."""

        mapping = {
            self.Status.DRAFT: "Under review by admin",
            self.Status.PUBLISHED: "Approved & Live",
            self.Status.ARCHIVED: "Rejected by admin",
        }

        return mapping.get(self.status, "Unknown")
    


class CommentQuerySet(models.QuerySet):
    """
    Semantic query interface for comments.
    """

    def approved(self):
        """Return only approved comments — visible to public."""
        return self.filter(is_approved=True)

    def pending(self):
        """Return comments waiting for admin approval."""
        return self.filter(is_approved=False)


class Comment(models.Model):
    """
    Blog comment — supports both guest and authenticated users.
    Requires admin approval before becoming publicly visible.
    """

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
    )

    # optional — None means guest comment
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,  # keep comment even if user is deleted
        null=True,
        blank=True,
        related_name="comments",
    )

    name = models.CharField(max_length=150)
    email = models.EmailField(blank=True)  # optional for logged-in users
    message = models.TextField()

    is_approved = models.BooleanField(default=False)  # admin must approve before visible
    created_date = models.DateTimeField(auto_now_add=True)

    objects = CommentQuerySet.as_manager()

    class Meta:
        ordering = ["-created_date"]

    def __str__(self):
        return f"{self.name} → {self.post.title}"
    



class Like(models.Model):
    """
    Represents a "like" action performed by a user on a post.
    """

    # The user who liked the post
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="likes"
    )

    # The post that was liked
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="likes"
    )

    # Timestamp of when the like was created
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        # newest likes first
        ordering = ["-created_date"]

        # prevent duplicate likes (same user cannot like same post twice)
        unique_together = ("user", "post")

    def __str__(self):
        return f"{self.user} liked {self.post}"
    

class SavedPost(models.Model):
    # Represents a "saved/bookmarked" post by a user.
    # User who saved the post
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='saved_posts')
    # Post that was saved
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='saved_by')
    # When the post was saved
    created_date = models.DateTimeField(auto_now_add=True)
    class Meta:
        # newest saved items first
        ordering = ["-created_date"]
        # prevent duplicate saves
        unique_together = ("user", "post")
    def __str__(self):
        return f"{self.user} saved {self.post}"