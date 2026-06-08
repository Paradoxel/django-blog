from django.db import models

class Contact(models.Model):
    name=models.CharField(max_length=150)
    email=models.EmailField()
    subject=models.CharField(max_length=150)
    message=models.TextField()
    created_date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"

    class Meta:
        ordering=['-created_date']





class Position(models.TextChoices):
    SIDEBAR = "sidebar", "Sidebar"
    POST = "post", "Post Detail"
    FOOTER = "footer", "Footer"


class Ad(models.Model):
    """
    Simple advertisement model for sidebar display.
    """

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

    def has_link(self):
        return bool(self.url)
    

class Newsletter(models.Model):
    email=models.EmailField(unique=True)
    created_date=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-created_date']
    
    def __str__(self):
        return self.email