from django.contrib import admin
from django.utils import timezone
from .models import (Category, 
                    Tag,
                    Post,
                    Comment,
                    Like,
                    SavedPost)


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

    def likes_count(self,obj):
        return obj.likes.count()
    
    actions=[
        'approve_posts',
        'reject_posts',
    ]
    @admin.action(description="Approve selected posts")
    def approve_posts(self,request,queryset):
        for post in queryset:
            post.status=Post.Status.PUBLISHED
            post.save()

    @admin.action(description="Reject selected posts")
    def reject_posts(self,request,queryset):
        queryset.update(status=Post.Status.ARCHIVED)



@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Admin configuration for Comment model."""

    list_display = ('name', 'post', 'is_approved', 'created_date')
    list_filter = ('is_approved',)
    search_fields = ('name', 'email', 'message')



class UserPostRelationAdmin(admin.ModelAdmin):
    list_display = ("user", "post", "created_date")
    search_fields = ("user__username", "post__title")
    list_filter = ("created_date",)
    ordering = ("-created_date",)

@admin.register(SavedPost)
class SavedPostAdmin(UserPostRelationAdmin):
    pass    

@admin.register(Like)
class LikeAdmin(UserPostRelationAdmin):
    pass