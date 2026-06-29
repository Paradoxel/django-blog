from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.conf import settings
from .managers import UserManager
from .validators import validate_iran_phone_number


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model that uses email as the unique identifier
    instead of the default username field.
    """

    email = models.EmailField(unique=True)  # used as USERNAME_FIELD
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)  # set False to deactivate without deleting
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # no extra fields required on createsuperuser

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        """Return full name, or email if first/last name are not set."""
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name or self.email


def avatar_upload_path(instance, filename):
    """Generate a unique upload path per user: avatars/<user_id>/<filename>"""
    return f"avatars/{instance.user.id}/{filename}"





# type of user
class UserTypes(models.TextChoices):
    READER = "reader", "Reader"
    WRITER = "writer", "Writer"
class Profile(models.Model):
    """
    Extended user profile created automatically via signal on User creation.
    Stores optional personal info and social links.
    """

    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )

    user_type = models.CharField(
        max_length=20,
        choices=UserTypes.choices,
        default=UserTypes.READER
    )

    phone_number = models.CharField(
        max_length=13,
        blank=True,
        null=True,
        unique=True,
        validators=[validate_iran_phone_number],  # accepts 09xx or +989xx format
    )

    avatar = models.ImageField(
        upload_to=avatar_upload_path,
        blank=True,
        null=True,
    )

    bio = models.CharField(max_length=150, blank=True)

    # social links — all optional
    website = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()}'s profile"
    












class Status(models.TextChoices):
    PENDING  = 'pending',  'Pending'
    APPROVED = 'approved', 'Approved'
    REJECTED = 'rejected', 'Rejected'

class WriterRequest(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    status = models.CharField(max_length=10,choices=Status.choices,default=Status.PENDING)
    reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True,blank=True)
