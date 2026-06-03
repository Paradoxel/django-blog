from django.contrib import admin
from .models import Contact

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display=['name','email','subject','created_date']
    search_fields=['name','email','subject']
    date_hierarchy='created_date'