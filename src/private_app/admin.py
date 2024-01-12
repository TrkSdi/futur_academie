# Third-party imports
from django.contrib import admin

# Local imports
from .models import Address, UserProfile, User, Link


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


class UserProfileInline(admin.TabularInline):
    model = UserProfile
    extra = 1


class UserAdmin(admin.ModelAdmin):
    # list_display = ('id', "user", "image_profile",
    #                 "url_tiktok", "url_instagram", "about_me", "is_public", "student_at")
    list_display = ('username', 'first_name', 'last_name', 'email', )
    list_filter = ('first_name', 'last_name', 'email', )
    # I wanted to add LinkInline but it's not a foreign key
    inlines = [UserProfileInline, ]


admin.site.register(Address, AddressAdmin)
admin.site.register(User, UserAdmin)
