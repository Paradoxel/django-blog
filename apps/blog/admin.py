from django.contrib import admin

from .models import Category, Tag, Post, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin configuration for Category model."""

    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Admin configuration for Tag model."""

    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Admin configuration for Post model."""

    list_display = ('title', 'author', 'status', 'view_count', 'published_date')
    search_fields = ('title', 'content', 'author__email')  
    list_filter = ('status',)  
    date_hierarchy = 'created_date'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Admin configuration for Comment model."""

    list_display = ('name', 'post', 'is_approved', 'created_date')
    list_filter = ('is_approved',)
    search_fields = ('name', 'email', 'message')