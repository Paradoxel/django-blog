from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps.views import sitemap

from apps.core.sitemaps import StaticViewSitemap
from apps.blog.sitemaps import (
    BlogIndexSitemap,
    BlogPostSitemap,
    BlogCategorySitemap,
    BlogTagSitemap,
    BlogAuthorSitemap,
)

sitemaps = {
    "static": StaticViewSitemap,
    "blog-index": BlogIndexSitemap,
    "blog-posts": BlogPostSitemap,
    "blog-categories": BlogCategorySitemap,
    "blog-tags": BlogTagSitemap,
    "blog-authors": BlogAuthorSitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.core.urls")),
    path("blog/", include("apps.blog.urls")),
    path('accounts/',include("apps.accounts.urls")),
    path("captcha/", include("captcha.urls")),
    path("sitemap.xml/", sitemap, {"sitemaps": sitemaps}),
    path("robots.txt", include("robots.urls")),
]

# Serve media files in development only
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )