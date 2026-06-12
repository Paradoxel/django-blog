from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from apps.core.sitemaps import StaticViewSitemap
from apps.blog.sitemaps import BlogIndexSitemap,BlogPostSitemap
sitemaps = {
    "static": StaticViewSitemap,
    "blog":BlogIndexSitemap,
    "blog-posts": BlogPostSitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.core.urls")),
    path("blog/", include("apps.blog.urls")),
    path("captcha/", include("captcha.urls")),
    path("sitemap-static.xml/", sitemap, {"sitemaps": {"static": StaticViewSitemap}}),
    path("sitemap-blog.xml/", sitemap, {"sitemaps": {"blog-posts": BlogPostSitemap}}),
]

# Serve media files in development only
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )