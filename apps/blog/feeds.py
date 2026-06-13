from django.contrib.syndication.views import Feed
from .models import Post


class LatestPostsFeed(Feed):
    """RSS feed for the latest published blog posts."""

    # Feed metadata shown in RSS readers
    title = "Django Blog — Latest Posts"
    link = "/blog/"
    description = "Latest posts from the blog."

    def items(self):
        # Return latest published posts (limited to 20 items)
        return Post.objects.published()[:20]

    def item_title(self, item):
        # Title of each RSS item
        return item.title

    def item_description(self, item):
        # Description: use excerpt if available, otherwise truncate content
        return item.excerpt or item.content[:300]

    def item_link(self, item):
        # URL to the full blog post
        return item.get_absolute_url()

    def item_pubdate(self, item):
        # Publication date for RSS sorting
        return item.published_date