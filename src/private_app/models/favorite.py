from django.db import models
import uuid


class Favorite(models.Model):
    """A model for users to save programs to a favorite list, write a personal note about the choice,
    and eventually share their program choices with others."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        related_name="favorites",
        null=False,
        help_text="FK to the user who created the favorite.",
    )
    study_program = models.ForeignKey(
        "StudyProgram",
        related_name="favorite",
        on_delete=models.CASCADE,
        null=False,
        help_text="The program saved as a favorite by the user.",
    )

    note = models.CharField(
        max_length=300,
        help_text="A private note written by the user about the program.",
        null=True,
    )

    APPLIED = "applied"
    ACCEPTED = "accepted"
    WAITLISTED = "waitlisted"
    ENROLLED = "enrolled"

    STATUS_CHOICES = [
        (APPLIED, "applied"),
        (ACCEPTED, "accepted"),
        (WAITLISTED, "waitlisted"),
        (ENROLLED, "enrolled"),
    ]

    status = models.CharField(
        choices=STATUS_CHOICES,
        help_text="The status of the student's application, if they apply.",
    )
