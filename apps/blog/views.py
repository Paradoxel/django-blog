from django.views.generic import ListView, DetailView

from apps.blog.models import Post
from django.db.models import Q

class BlogView(ListView):
    """
    Display paginated list of published blog posts.
    """

    template_name = "blog/blog-home.html"
    context_object_name = "posts"
    paginate_by = 6

    # Use Walrus :=
    def get_queryset(self):
        posts=Post.objects.published()
        if s:=self.request.GET.get("search",""):
            posts=posts.filter(Q(title__icontains=s) | Q(excerpt__icontains=s))
        return posts
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get("search","")
        return context


class PostDetailView(DetailView):
    """
    Display a single published post by slug.
    Increments view_count on each visit.
    """

    model = Post
    template_name = "blog/blog-single.html"
    context_object_name = "post"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        # Only published posts are accessible — drafts return 404
        return Post.objects.published()

    def get_object(self, queryset=None):
        post = super().get_object(queryset)
        # Increment view count on every visit
        Post.objects.filter(pk=post.pk).update(view_count=post.view_count + 1)
        return post