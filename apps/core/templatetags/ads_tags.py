from django import template
from apps.core.models import Ad

register = template.Library()


@register.inclusion_tag("blog/partials/ads_widget.html")
def ads_widget():
    ad = Ad.objects.filter(is_active=True).first()

    return {"ad": ad}