from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils import timezone

from .models import (
    Profile,
    Status,
    User,
    UserTypes,
    WriterRequest,
)

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Admin configuration for the custom User model.
    Extends BaseUserAdmin to support email-based authentication
    instead of the default username-based setup.
    """

    # Display columns in the user list page
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

    # Fields shown when editing an existing user
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    # Fields shown when creating a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Admin configuration for the Profile model."""

    list_display = (
        "user",
        "user_type",
        "phone_number",
        "created_date",
    )

    search_fields = (
        "user__email",
        "phone_number",
    )

    list_filter = (
        "user_type",
        "created_date",
    )

    readonly_fields = (
        "created_date",
        "updated_date",
    )

    ordering = ("-created_date",)

    date_hierarchy = "created_date"






@admin.register(WriterRequest)
class WriterRequestAdmin(admin.ModelAdmin):
    """Admin configuration for writer requests."""

    list_display = [
        "user",
        "status",
        "created_at",
        "reviewed_at",
    ]

    search_fields = [
        "user__email",
        "reason",
    ]

    list_filter = [
        "status",
    ]

    readonly_fields = (
        "status",
        "created_at",
        "reviewed_at",
    )

    ordering = ("-created_at",)
    date_hierarchy = "created_at"

    actions = [
        "approve_requests",
        "reject_requests",
    ]

    @admin.action(description="Approve selected writer requests")
    def approve_requests(self, request, queryset):
        queryset.update(
            status=Status.APPROVED,
            reviewed_at=timezone.now(),
        )

        for writer_request in queryset:
            profile = writer_request.user.profile
            profile.user_type = UserTypes.WRITER
            profile.save(update_fields=["user_type"])

    @admin.action(description="Reject selected writer requests")
    def reject_requests(self, request, queryset):
        queryset.update(
            status=Status.REJECTED,
            reviewed_at=timezone.now(),
        )

        for writer_request in queryset:
            profile = writer_request.user.profile
            profile.user_type = UserTypes.READER
            profile.save(update_fields=["user_type"])
