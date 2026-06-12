from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.contrib.auth import get_user_model

from apps.blog.models import Post, Category, Tag

User = get_user_model()


class BlogIndexSitemap(Sitemap):
    # Blog homepage sitemap (static page)
    # Helps search engines know this page exists and is important
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        # Only include blog home page
        return ["blog:index"]

    def location(self, item):
        # Convert URL name into real URL path
        return reverse(item)


class BlogPostSitemap(Sitemap):
    # Blog post detail pages (dynamic content)
    # Each published post will appear in sitemap
    def items(self):
        return Post.objects.published()

    def location(self, item):
        # Use model's get_absolute_url() for clean URL handling
        return item.get_absolute_url()


class BlogCategorySitemap(Sitemap):
    # Category pages sitemap
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        # Include all categories
        return Category.objects.all()

    def location(self, obj):
        # Reverse URL for category page using slug
        return reverse("blog:category", kwargs={"slug": obj.slug})


class BlogTagSitemap(Sitemap):
    # Tag pages sitemap
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        # Include all tags
        return Tag.objects.all()

    def location(self, obj):
        # Reverse URL for tag page using slug
        return reverse("blog:tag", kwargs={"slug": obj.slug})


class BlogAuthorSitemap(Sitemap):
    # Author pages sitemap
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        # Only users who have written posts
        return User.objects.filter(posts__isnull=False).distinct()

    def location(self, obj):
        # Reverse URL for author page using primary key
        return reverse("blog:author", kwargs={"pk": obj.pk})