from django.contrib import admin
from .models import Profile, KYC


class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "pkid",
        "user",
        "phone_number",
        "is_verified",  # Add is_verified to the list display
        "country",
        "city",
        "is_seller",
        "is_agent",
    ]
    list_filter = [
        "country",
        "city",
        "is_verified",  # Add is_verified to the list filter
        "is_seller",
        "is_agent",
    ]
    list_display_links = ["id", "pkid", "user"]
    search_fields = [
        "user__username",
        "phone_number",
        "city",
    ]  # Optional: Add search functionality
    actions = ["mark_as_verified", "mark_as_unverified"]  # Add custom actions

    def mark_as_verified(self, request, queryset):
        queryset.update(is_verified=True)

    mark_as_verified.short_description = "Mark selected profiles as verified"

    def mark_as_unverified(self, request, queryset):
        queryset.update(is_verified=False)

    mark_as_unverified.short_description = "Mark selected profiles as unverified"


class KYCAdmin(admin.ModelAdmin):
    list_display = ["id", "pkid", "profile", "kyc_verified", "kyc_verified_at"]
    list_filter = ("kyc_verified",)
    list_display_links = ["id", "pkid", "profile"]
    search_fields = ["profile__user__username"]  # Optional: Add search functionality


# Register models separately
admin.site.register(Profile, ProfileAdmin)
admin.site.register(KYC, KYCAdmin)
