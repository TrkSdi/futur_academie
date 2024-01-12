# Third-party imports
from django.contrib import admin

# Local imports
from .models import Address,Favorite


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
    
    
    
admin.site.register(Address, AddressAdmin)
admin.site.register(Favorite, FavoriteAdmin)