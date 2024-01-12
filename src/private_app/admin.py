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


class SchoolAdmin(admin.ModelAdmin):
    list_display = (
        'UAI_code',
        'name',
        'school_url',
        'description',
        'address',
        'school_type'
    )
    list_filter = (
        'school_type'
    )
    search_fields = ('name', 'school_type')
    