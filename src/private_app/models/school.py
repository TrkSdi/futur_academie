from django.db import models


class School(models.Model):
    """A model for general information about the schools in which students may enroll."""

    UAI_code = models.CharField(max_length=12, primary_key=True)

    name = models.CharField(
        max_length=150, help_text="The name of the school or university."
    )

    school_url = models.OneToOneField(
        "Link",
        related_name="school",
        on_delete=models.CASCADE,
        help_text="A url to the school's website.",
        null=True,
        blank=True,
    )

    description = models.TextField(
        help_text="A short description of the school or university."
    )

    address = models.OneToOneField(
        "Address",
        related_name="school",
        on_delete=models.CASCADE,
        help_text="The school's address and GPS location.",
    )

    PUBLIC = "public"
    PRIVATE = "private"
    SCHOOL_TYPES = [(PUBLIC, "public"), (PRIVATE, "private")]
    school_type = models.CharField(
        choices=SCHOOL_TYPES, help_text="Type of school, public or private."
    )

    def __str__(self) -> str:
        return f"{self.name}"
