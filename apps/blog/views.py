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
        posts = Post.objects.published()

        # search filter
        if s := self.request.GET.get("search", ""):
            posts = posts.filter(Q(title__icontains=s) | Q(excerpt__icontains=s))

        # category/tag filter — only when slug exists in URL
        if slug := self.kwargs.get("slug"):
            if "category" in self.request.path:
                posts = posts.filter(categories__slug=slug)
            elif "tag" in self.request.path:
                posts = posts.filter(primary_tag__slug=slug)
        if pk:=self.kwargs.get('pk'):
            posts=posts.filter(author__pk=pk)
        return posts
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get("search","")
        # pass active category to template for highlighting
        if category_slug := self.kwargs.get("slug"):
            context["active_category"] = category_slug
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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post=self.get_object()
        context["next_post"] = Post.objects.published().filter(id__gt=post.id).order_by('id').first()
        context["previous_post"] = Post.objects.published().filter(id__lt=post.id).order_by('-id').first()
        return context