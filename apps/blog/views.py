from django.shortcuts import render
from django.views.generic import ListView,DetailView
from apps.blog.models import Post
class BlogView(ListView):
    template_name='blog/blog-home.html'
    context_object_name='posts'
    def get_queryset(self):
        return Post.objects.published()

class PostDetailView(DetailView):
    model = Post
    template_name = "blog/blog-single.html"
    context_object_name = "post"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return Post.objects.published()