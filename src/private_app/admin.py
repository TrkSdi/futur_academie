# Third-party imports
from django.contrib import admin

# Local imports
from .models import Address


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
