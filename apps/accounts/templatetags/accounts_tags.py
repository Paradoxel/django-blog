from django import template
register = template.Library()
@register.inclusion_tag("accounts/partials/sidebar.html")
def user_sidebar(user):
    return {'user':user}

