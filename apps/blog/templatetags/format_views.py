from django import template


register = template.Library()


@register.filter
def format_views(value):
    """Format view count: 1500 → 1.5K, 1500000 → 1.5M."""
    try:
        value = int(value)
    except (TypeError, ValueError):
        return value

    if value >= 1_000_000:
        return f"{value / 1_000_000:.1f}M"
    if value >= 1_000:
        return f"{value / 1_000:.1f}K"
    return value