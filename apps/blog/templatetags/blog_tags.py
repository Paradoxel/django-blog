from django import template
from apps.blog.models import Post
from apps.blog.models import Category
register = template.Library()
@register.inclusion_tag("blog/partials/popular_posts.html")
def popular_posts():
    posts=Post.objects.filter(status=Post.Status.PUBLISHED).order_by("-view_count", "-published_date")[:4]
    return {"popular_posts": posts}



@register.inclusion_tag("blog/partials/author_widget.html")
def author_widget(author):
    return {'author':author}


@register.inclusion_tag("blog/partials/category_widget.html")
def category_widget():
    categories = Category.objects.all()

    for cat in categories:
        cat.post_count = Post.objects.published().filter(categories=cat).count()
    # sort
    categories = sorted(categories, key=lambda c: c.post_count, reverse=True)

    return {
        "categories": categories
    }