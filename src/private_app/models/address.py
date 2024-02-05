from django.db import models
from django.contrib.gis.db import models as gismodels


class Address(models.Model):
    """A model for storing school/program addresses and GPS locations."""

    street_address = models.CharField(
        help_text="Building number and street name of the address.",
        max_length=100,
        null=True,
        blank=True,
    )
    postcode = models.PositiveIntegerField(
        help_text="Post code for the address.", null=True, blank=True
    )
    locality = models.CharField(
        help_text="The city and more precise locality info (as required) for the address.",
        max_length=100,
        null=True,
        blank=True,
    )
    geolocation = gismodels.PointField(
        help_text="Longitude and latitude of the address's location.",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.locality}, {self.postcode}, {self.street_address}"

    class Meta:
        verbose_name_plural = "Addresses"
