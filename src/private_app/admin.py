# Third-party imports
from django.contrib import admin

# Local imports
from .models import Address, Link, Favorite, School, StudyProgram, UserProfile, User


class AddressAdmin(admin.ModelAdmin):
    list_display = (
        "street_address",
        "postcode",
        "locality",
        "geolocation",
    )
    list_filter = ("locality",)
    search_fields = ("postcode", "locality",)


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("user", "study_program", "note", "status",)
    list_filter = ("study_program", "status",)
    search_fields = ("note",)
    list_per_page = 10


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
        'school_type',
    )
    search_fields = ('name', 'school_type')


class StudyProgramAdmin(admin.ModelAdmin):
    list_display = (
        "cod_aff_form",
        "name",
        "school",
        "discipline",
        "acceptance_rate",
        "L1_success_rate",
        "insertion_rate",
        "insertion_time_period"
    )
    list_filter = ("discipline", "school")
    search_fields = ("name", "cod_aff_form", "description")


admin.site.register(Address, AddressAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(StudyProgram, StudyProgramAdmin)
admin.site.register(User, UserAdmin)
