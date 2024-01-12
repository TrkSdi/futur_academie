# Third-party imports
from django.contrib import admin

# Local imports
from .models import Address, Link


class AddressAdmin(admin.ModelAdmin):
    list_display = (
        "street_address",
        "postcode",
        "locality",
        "geolocation",
    )
    list_filter = ("locality",)
    search_fields = ("postcode", "locality")


admin.site.register(Address, AddressAdmin)


class LinkAdmin(admin.ModelAdmin):
    list_display = ("link_type", "link_url")
    list_filter = ("link_type",)
    search_fields = ("link_url",)


admin.site.register(Link, LinkAdmin)
