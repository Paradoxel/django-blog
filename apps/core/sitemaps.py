from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class StaticViewSitemap(Sitemap):
    # How often search engines should expect this page to change
    changefreq = "monthly"

    # Priority of these pages compared to other pages on your site (0.0 - 1.0)
    priority = 0.8

    def items(self):
        # List of URL names (using namespace: core)
        return [
            "core:home",
            "core:about",
            "core:contact",
        ]

    def location(self, item):
        # Convert URL name into actual URL path
        return reverse(item)