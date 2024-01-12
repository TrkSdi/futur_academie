from django.db import models


class Link(models.Model):
    """A model to store links to user and school websites."""

    SOCIAL_TYPE = [
        ("Website", "Website"),
        ("Facebook", "Facebook"),
        ("Twitter", "Twitter"),
        ("Instagram", "Instagram"),
        ("Autres", "Autres"),
    ]  # every social media
    link_type = models.CharField(
        max_length=30,
        choices=SOCIAL_TYPE,
        help_text="Type of website (Instagram, FB, etc.)",
    )
    link_url = models.CharField(
        max_length=100, null=True, blank=True, help_text="URL to the website"
    )

    def __str__(self):
        link = self.link_url
        # if len(link) > 30:
        #     link = link[0:30] + "..."
        return f"{link}"
