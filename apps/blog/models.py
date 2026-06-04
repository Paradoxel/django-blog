from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


# Content tags
class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True, db_index=True)

    def save(self, *args, **kwargs):
        # Auto-generate slug
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# Hierarchical categories
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True, db_index=True)
    description = models.TextField(blank=True)

    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="children"
    )

    class Meta:
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        # Auto-generate slug
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# Custom post filters
class PostQuerySet(models.QuerySet):

    def published(self):
        return self.filter(status=Post.Status.PUBLISHED)

    def drafts(self):
        return self.filter(status=Post.Status.DRAFT)

    def archived(self):
        return self.filter(status=Post.Status.ARCHIVED)


class Post(models.Model):

    # Publication status
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"
        ARCHIVED = "archived", "Archived"

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts"
    )

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, db_index=True)

    content = models.TextField()

    image = models.ImageField(upload_to="images/")

    primary_tag = models.ForeignKey(
        Tag,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="primary_posts"
    )

    categories = models.ManyToManyField(
        Category,
        related_name="posts"
    )

    view_count = models.PositiveIntegerField(default=0)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
        db_index=True
    )

    published_date = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True
    )

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    objects = PostQuerySet.as_manager()

    class Meta:
        ordering = ["-published_date", "-created_date"]

    def save(self, *args, **kwargs):

        # Generate unique slug
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1

            while Post.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        # Set publish timestamp
        if (
            self.status == self.Status.PUBLISHED
            and self.published_date is None
        ):
            self.published_date = timezone.now()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title}"