from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse


class Tag(models.Model):
    """Content tag for labeling posts."""

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=255,unique=True, blank=True) 

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Category(models.Model):
    """
    Post category.
    Per Post Many Category
    """

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=255,unique=True, blank=True) 
    description = models.TextField(blank=True)

    class Meta:
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
    Handles draft → published → archived workflow.
    Auto-generates slug and sets published_date on first publish.
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
    slug = models.SlugField(max_length=255,unique=True, blank=True)  

    content = models.TextField()
    excerpt = models.CharField(max_length=300, blank=True)  # short preview 

    # organized by year/month to avoid too many files in one folder
    image = models.ImageField(upload_to="posts/%Y/%m/")

    primary_tag = models.ForeignKey(
        Tag,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="primary_posts",
    )

    categories = models.ManyToManyField(
        Category,
        related_name="posts",
    )

    view_count = models.PositiveIntegerField(default=0)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
        db_index=True,  # frequently filtered — index justified
    )

    published_date = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True,  # used in ordering and filters — index justified
    )

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    objects = PostQuerySet.as_manager()

    class Meta:
        ordering = ["-created_date"]

    def save(self, *args, **kwargs):
        # Build unique slug from title on first save only
        if not self.slug:
            base_slug = slugify(self.title[:240])
            slug = base_slug
            counter = 1

            while Post.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        # Auto-set published_date once on first publish — never overwrite
        if self.status == self.Status.PUBLISHED:
            if not self.published_date:
                self.published_date = timezone.now()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("blog:detail", kwargs={"slug": self.slug})
    
    def reading_time(self):
        """Estimate reading time based on average 200 words per minute."""
        word_count = len(self.content.split())
        minutes = max(1, round(word_count / 200))
        return minutes
    


class CommentQuerySet(models.QuerySet):
    """Semantic filters for comment moderation and display."""

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