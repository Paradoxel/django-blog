from django.db import models


class Contact(models.Model):
    """Stores messages submitted via the contact form."""

    name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=150)
    message = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_date"]

    def __str__(self):
        return f"{self.name} - {self.subject}"


class Ad(models.Model):
    """Advertisement displayed in the sidebar."""

    title = models.CharField(max_length=100)
    description = models.CharField(max_length=150, blank=True)
    image = models.ImageField(upload_to="ads/")
    url = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_date"]

    def __str__(self):
        return self.title


class Newsletter(models.Model):
    """Stores newsletter subscriber emails."""

    email = models.EmailField(unique=True)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_date"]

    def __str__(self):
        return self.email