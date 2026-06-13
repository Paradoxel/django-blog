from django import template
from django.db.models import Count
from django.db import models
from apps.blog.models import Post, Category, Tag


register = template.Library()


@register.inclusion_tag("blog/partials/popular_posts.html")
def popular_posts():
    """Return top 4 posts ordered by view count."""
    posts = Post.objects.published().order_by("-view_count", "-published_date")[:4]
    return {"popular_posts": posts}


@register.inclusion_tag("blog/partials/author_widget.html")
def author_widget(author):
    """Render author info widget for post detail sidebar."""
    return {"author": author}


@register.inclusion_tag("blog/partials/category_widget.html")
def category_widget():
    """
    Return categories with published post counts.
    annotate() runs a single SQL JOIN instead of N+1 queries.
    """
    categories = (
        Category.objects
        .annotate(
            post_count=Count(
                "posts",
                filter=models.Q(posts__status=Post.Status.PUBLISHED)
            )
        )
        .order_by("-post_count")
    )
    return {"categories": categories}


@register.inclusion_tag("blog/partials/post_categories.html")
def post_categories(post):
    """Return categories belonging to a specific post."""
    return {"categories": post.categories.all()}


@register.inclusion_tag("blog/partials/tag_widget.html")
def tag_widget():
    """Return all tags for the tag cloud widget."""
    tags = Tag.objects.all()
    return {"tags": tags}


@register.inclusion_tag('blog/partials/related_posts.html')
def related_posts(post):
    """Return up to 3 published posts sharing categories with the given post."""
    posts=Post.objects.published().filter(
        categories__in=post.categories.all()
    ).exclude(pk=post.pk).distinct().order_by('-view_count')[:3]
    return {'related_posts': posts}  