from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from .models import Profile


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance, created, **kwargs):
    """Auto-create Profile on new User creation. Skips on update."""
    if created:
        Profile.objects.create(user=instance)