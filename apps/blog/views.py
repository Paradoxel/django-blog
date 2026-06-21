from django.contrib import messages
from django.db.models import Q, F
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView,View
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.blog.models import Post,Like,SavedPost
from apps.blog.forms import CommentForm


class BlogView(ListView):
    """
    Display paginated list of published blog posts.
    Supports search, category, tag, and author filters.
    """

    template_name = "blog/blog-home.html"
    context_object_name = "posts"
    paginate_by = 6

    def get_queryset(self):
        posts = Post.objects.published()

        if s := self.request.GET.get("search", ""):
            posts = posts.filter(Q(title__icontains=s) | Q(excerpt__icontains=s))

        if slug := self.kwargs.get("slug"):
            if "category" in self.request.path:
                posts = posts.filter(categories__slug=slug)
            elif "tag" in self.request.path:
                posts = posts.filter(primary_tag__slug=slug)

        if pk := self.kwargs.get("pk"):
            posts = posts.filter(author__pk=pk)

        return posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("search", "")
        if slug := self.kwargs.get("slug"):
            context["active_slug"] = slug
        return context


class PostDetailView(DetailView):
    """
    Display a single published post by slug.
    Increments view_count on GET only.
    Handles comment submission via POST.
    """

    model = Post
    template_name = "blog/blog-single.html"
    context_object_name = "post"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return Post.objects.published()

    def get_object(self, queryset=None):
        post = super().get_object(queryset)
        if self.request.method == "GET":
            Post.objects.filter(pk=post.pk).update(view_count=F("view_count") + 1)
        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object

        if self.request.user.is_authenticated:
            user = self.request.user

            context["is_liked"] = post.likes.filter(user=user).exists()
            context["is_saved"] = post.saved_by.filter(user=user).exists()
        else:
            context["is_liked"] = False
            context["is_saved"] = False

        context["likes_count"] = post.likes.count()

        context["next_post"] = (
            Post.objects.published()
            .filter(published_date__gt=post.published_date)
            .order_by("published_date")
            .first()
        )

        context["previous_post"] = (
            Post.objects.published()
            .filter(published_date__lt=post.published_date)
            .order_by("-published_date")
            .first()
        )

        context["comments"] = post.comments.approved()
        context["comment_form"] = CommentForm()

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            # attach user if logged in, otherwise guest comment
            comment.user = request.user if request.user.is_authenticated else None
            comment.save()
            messages.success(
                request,
                "Your comment has been submitted and will be visible after approval."
            )
            return redirect("blog:detail", slug=self.object.slug)

        # re-render form with validation errors
        context = self.get_context_data()
        context["comment_form"] = form
        return self.render_to_response(context)
    


class ToggleLikeView(LoginRequiredMixin,View):
    def post(self,request,slug):
        post=get_object_or_404(Post,slug=slug)
        like=post.likes.filter(user=request.user).first()
        if like:
            like.delete()
        else:
            post.likes.create(user=request.user)
        return redirect("blog:detail",slug=slug)
    

class ToggleSaveView(LoginRequiredMixin,View):
    def post(self,request,slug):
        post=get_object_or_404(Post,slug=slug)
        saved=post.saved_by.filter(user=request.user).first()
        if saved:
            saved.delete()
        else:
            post.saved_by.create(user=request.user)
        return redirect("blog:detail",slug=post.slug)
