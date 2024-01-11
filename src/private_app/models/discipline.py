from django.db import models


class Discipline(models.Model):
    """A model to organize programs by the general discipline."""

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
