from django.contrib import admin
from .models import Contact,Ad

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display=['name','email','subject','created_date']
    search_fields=['name','email','subject']
    date_hierarchy='created_date'


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "is_active",
        "created_date",
    )
    list_filter = (
        "is_active",
    )
    search_fields = (
        "title",
    )
    list_per_page=10
