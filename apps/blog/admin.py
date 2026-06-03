from django.contrib import admin
from .models import Category, Tag, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name', 'slug']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name', 'slug']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        'author',
        'title',
        'view_count',
        'status',
        'published_date'
    ]

    search_fields = [
        'title',
        'content',
        'author__username'
    ]

    list_filter = [
        'author',
        'status'
    ]

    date_hierarchy = 'created_date'