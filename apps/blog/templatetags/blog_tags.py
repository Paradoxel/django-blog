from django import template
from apps.blog.models import Post
from apps.core.models import Ad
register = template.Library()
@register.inclusion_tag("blog/partials/popular_posts.html")
def popular_posts():
    posts=Post.objects.filter(status=Post.Status.PUBLISHED).order_by("-view_count", "-published_date")[:4]
    return {"popular_posts": posts}



@register.inclusion_tag("blog/partials/author_widget.html")
def author_widget(author):
    return {'author':author}