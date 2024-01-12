# Third-party imports
from django.contrib import admin

# Local imports
from .models import StudyProgram


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


admin.site.register(StudyProgram, StudyProgramAdmin)
