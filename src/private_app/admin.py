# Third-party imports
from django.contrib import admin

# Local imports
from .models import Address, UserProfile


class AddressAdmin(admin.ModelAdmin):
    list_display = (
        "street_address",
        "postcode",
        "locality",
        "geolocation",
    )
    list_filter = ("locality",)
    search_fields = ("postcode", "locality")


class LinkInline(admin.TabularInline):
    model = Link
    extra = 1


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', "user", "image_profile",
                    "url_tiktok", "url_instagram", "about_me", "is_public", "student_at")
    list_filter = ("user", "student_at", "is_public",)
    search_fields = ("user", "student_at", "about_me")
    inlines = [LinkInline]


admin.site.register(Address, AddressAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
