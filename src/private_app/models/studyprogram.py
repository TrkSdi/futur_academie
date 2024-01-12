from django.db import models


class StudyProgram(models.Model):
    """A model for information on specific programs of study to which students may apply."""

    cod_aff_form = models.IntegerField(
        primary_key=True, help_text="Parcoursup code for the program"
    )

    name = models.CharField(
        max_length=100,
        help_text="The name of the program of study.",
        null=False,
    )
    school = models.ForeignKey(
        "School",
        on_delete=models.CASCADE,
        related_name="study_programs",
        null=False,
        help_text="FK to the school which offers the program of study.",
    )

    DROIT = "Droit_Sc_Politiques"
    ECO = "Economie_AES"
    ARTS = "Arts_Lettres_Langues_SHS"
    SCIENCES = "Sciences_Sante"
    STAPS = "STAPS"
    AUTRES = "Autres"
    DISCIPLINE_TYPE = [
        (DROIT, "Droit Sc. politiques"),
        (ECO, "Économie, AES"),
        (ARTS, "Arts, lettres, langues, SHS"),
        (SCIENCES, "Sciences-santé"),
        (STAPS, "STAPS"),
        (AUTRES, "autres"),
    ]
    discipline = models.CharField(
        max_length=130,
        choices=DISCIPLINE_TYPE,
        help_text="Choice of the general discipline to which a program belongs.",
    )

    # URL en onetoone
    url_parcoursup = models.OneToOneField(
        "Link",
        related_name="study_program",
        on_delete=models.CASCADE,
        help_text="A url to the program's parcoursup page.",
    )

    acceptance_rate = models.FloatField(
        help_text="The percentage of applicants who are admitted to the program via parcoursup.",
        null=True,
    )
    L1_success_rate = models.FloatField(
        help_text="The percentage of first year students who validate both semesters.",
        null=True,
    )
    insertion_rate = models.FloatField(
        help_text="The percentage of graduates who are employeed a given period of time after graduating.",
        null=True,
    )
    insertion_time_period = models.PositiveIntegerField(
        help_text="The amount of time between graduation and the calculation of the insertion rate.",
        null=True,
    )
    description = models.TextField(help_text="The description of the program")
