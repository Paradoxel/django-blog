from django.conf import settings


def google_maps_key(request):
    """Inject Google Maps API key into all template contexts."""
    return {"GOOGLE_MAPS_API_KEY": settings.GOOGLE_MAPS_API_KEY}