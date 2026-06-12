from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from apps.blog.models import Post


class BlogIndexSitemap(Sitemap):
    # How often this page changes (SEO hint for search engines)
    changefreq = "weekly"

    # Priority of this page compared to other pages (0.0 - 1.0)
    priority = 0.8

    def items(self):
        # Only include the blog homepage
        return ["blog:index"]

    def location(self, item):
        # Convert named URL into actual URL path
        return reverse(item)


class BlogPostSitemap(Sitemap):
    def items(self):
        # Return all published blog posts
        return Post.objects.published()

    def location(self, item):
        # Use model's absolute URL (clean Django practice)
        return item.get_absolute_url()