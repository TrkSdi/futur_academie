from django.contrib.gis.db import models as gismodels
from django.db import models


class StudyProgram(models.Model):
    """A model for information on specific programs of study to which students may apply."""

    cod_aff_form = models.IntegerField(
        help_text="Parcoursup code for the program", primary_key=True
    )
    name = models.CharField(
        help_text="The name of the program of study.",
        max_length=100,
        null=False,
    )
    is_selective = models.BooleanField(
        help_text="True if the program is selective, false if it is non-selective.",
        null=True,
        blank=True,
    )
    city = models.CharField(
        help_text="City in which the program is located.",
        max_length=50,
        null=True,
        blank=True,
    )
    geolocation = gismodels.PointField(
        help_text="Longitude and latitude of the program location.",
        null=True,
        blank=True,
    )

    school = models.ForeignKey(
        "School",
        help_text="FK to the school which offers the program of study.",
        on_delete=models.CASCADE,
        related_name="study_programs",
        null=False,
    )

    url_parcoursup = models.OneToOneField(
        "Link",
        help_text="A url to the program's parcoursup page.",
        related_name="study_program",
        on_delete=models.CASCADE,
    )
    QUARTILES = (
        ("Q1", "Q1"),
        ("Q2", "Q2"),
        ("Q3", "Q3"),
        ("Q4", "Q4"),
    )
    acceptance_rate = models.FloatField(
        help_text="The percentage of applicants who are admitted to the program via parcoursup.",
        null=True,
        blank=True,
    )

    available_places = models.PositiveIntegerField(
        help_text="The number of students who can enroll in the program.",
        null=True,
        blank=True,
    )
    number_applicants = models.PositiveIntegerField(
        help_text="The number of students who applied to the program.",
        null=True,
        blank=True,
    )
    percent_scholarship = models.FloatField(
        help_text="The percentage of students who receive a government scholarship (boursiers).",
        null=True,
        blank=True,
    )
    out_of_sector_candidates = models.FloatField(
        help_text="The percentage of students from outside of the program's area who are admitted to the program.",
        null=True,
        blank=True,
    )
    L1_success_rate = models.FloatField(
        help_text="The percentage of first year students who validate both semesters.",
        null=True,
    )
    diploma_earned_ontime = models.FloatField(
        help_text="The percentage of students who complete the program within 3-4 years for a 'licence' or 2-3 years.",
        null=True,
        blank=True,
    )

    acceptance_rate_quartile = models.CharField(
        help_text="The quartile in which the acceptance rate falls compared to all programs",
        choices=QUARTILES,
        null=True,
        blank=True,
    )
    L1_success_rate_quartile = models.CharField(
        help_text="The quartile in which the percentage of students who continue to L2 falls compared to all programs",
        choices=QUARTILES,
        null=True,
        blank=True,
    )
    diploma_earned_ontime_quartile = models.CharField(
        help_text="The quartile in which the percentage of students who graduate on time falls compared to all programs",
        choices=QUARTILES,
        null=True,
        blank=True,
    )
    percent_scholarship_quartile = models.CharField(
        help_text="The quartile in which the percentage of scholarship studentsfalls compared to all programs",
        choices=QUARTILES,
        null=True,
        blank=True,
    )

    description = models.TextField(
        help_text="The description of the program scraped from the parcoursup website.",
        null=True,
        blank=True,
    )
    job_prospects = models.TextField(
        help_text="The job prospects of the program's graduates scraped from the parcoursup website.",
        null=True,
        blank=True,
    )
