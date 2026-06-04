from django.shortcuts import render
from django.views.generic import ListView
from apps.blog.models import Post
class BlogView(ListView):
    template_name='blog/blog-home.html'
    context_object_name='posts'
    def get_queryset(self):
        return Post.objects.published()

def blog_single(request):
    return render(request, 'blog/blog-single.html')