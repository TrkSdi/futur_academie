from django.db import models
from django.contrib.gis.db import models as gismodels


class Address(models.Model):
    """A model for storing school/program addresses and GPS locations."""

    street_address = models.CharField(
        max_length=100, help_text="Building number and street name of the address."
    )
    postcode = models.PositiveIntegerField(help_text="Post code for the address.")
    locality = models.CharField(
        max_length=100,
        help_text="The city and more precise locality info (as required) for the address.",
    )
    geolocation = gismodels.PointField(
        null=True,
        blank=True,
        help_text="Longitude and latitude of the address's location.",
    )

    def __str__(self):
        return f"{self.locality}, {self.postcode}, {self.street_address}"

    class Meta:
        verbose_name_plural = "Addresses"
