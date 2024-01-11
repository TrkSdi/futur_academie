from django.db import models
import uuid


class UserProfile(models.Model):
    """A model of user profiles which may be set to public
    to allow for interaction between students on the site."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.OneToOneField(
        "User",
        related_name="profile",
        on_delete=models.CASCADE,
        help_text="The profile's owner.",
    )

    # resize imagefield S3bucket qui externalise la gestion des images (pas pour le projet)
    image_profile = models.ImageField(
        upload_to="images_profile", help_text="Upload your photo", null=True, blank=True
    )

    # mettre onetoonefield
    url_tiktok = models.OneToOneField(
        "Link",
        related_name="profile",
        on_delete=models.CASCADE,
        help_text="A url to the user's TikTok profile.",
    )

    url_instagram = models.OneToOneField(
        "Link",
        related_name="profile",
        on_delete=models.CASCADE,
        help_text="A url to the user's Instagram profile.",
    )

    about_me = models.TextField(
        max_length=400, help_text="A profile description of the user."
    )
    is_public = models.BooleanField(
        default=False,
        help_text="True if the user agrees to make their profile public. False by default.",
    )
    student_at = models.ForeignKey(
        "StudyProgram",
        on_delete=models.SET_NULL,
        related_name="students",
        null=True,
        help_text="FK to a program the student in which the student is or has enrolled.",
    )

    # à revoir si intéressant
    prefered_disciplines = models.ManyToManyField(
        "Discipline",
        related_name="profiles",
        null=True,
        blank=True,
        help_text="Discipline choices of the student",
    )
