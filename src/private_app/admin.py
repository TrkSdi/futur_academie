# Third-party imports
from django.contrib import admin

# Local imports
from .models import Address, Link, Favorite, School


class AddressAdmin(admin.ModelAdmin):
    list_display = (
        "street_address",
        "postcode",
        "locality",
        "geolocation",
    )
    list_filter = ("locality",)
    search_fields = ("postcode", "locality")
    

class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("user","study_program","note","status")
    list_filter =("study_program","status")
    search_fields = ("note",)
    list_per_page = 10

class LinkAdmin(admin.ModelAdmin):
    list_display = ("link_type", "link_url")
    list_filter = ("link_type",)
    search_fields = ("link_url",)

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
    
admin.site.register(Address, AddressAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(School, SchoolAdmin)