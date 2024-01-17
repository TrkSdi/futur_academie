# Standard library imports
import json

# Third-party imports
from django.contrib.gis.geos import Point
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

# Local imports
from private_app.models import (
    Address,
    Link,
    School,
)


class Command(BaseCommand):
    help = "Importing data for school information"

    @transaction.atomic
    def handle(self, *args, **options):
        file_path = "C:/Users/rache/Sync/Formations/Diginamic/FilRouge/futur_academie/src/private_app/management/commands/fr-esr-principaux-etablissements-enseignement-superieur.json"
        with open(file_path, "r") as f:
            # Load the data
            data = json.load(f)
            # Loop through schools to ceate address, link and school objects for each
            for school in data:
                # If there is no UAI code, ignore the data
                if not school["uai"]:
                    break
                # Model requires a street address, so if none exists set it to NA, we can also alter the model
                if school["adresse_uai"]:
                    street_address = school["adresse_uai"]
                else:
                    street_address = "NA"

                locality = school["localite_acheminement_uai"]
                postcode = school["code_postal_uai"]
                longitude = school["coordonnees"]["lon"]
                latitude = school["coordonnees"]["lat"]
                # Create the point object with the GPS position
                coordinates = Point(x=longitude, y=latitude, srid=4326)

                # Create an address object with the given data
                address = Address.objects.create(
                    street_address=street_address,
                    locality=locality,
                    postcode=postcode,
                    geolocation=coordinates,
                )

                # If the school has a url, make a link object for it
                if school["url"]:
                    website = school["url"]
                    link = Link.objects.create(
                        link_type="SchoolWebsite", link_url=website
                    )
                else:
                    link = None

                name = school["uo_lib"]
                # CHANGE THIS AFTER DB IS UPDATED TO HOLD LARGER TEXT
                # until then cut names which are too long to fit
                if len(name) > 100:
                    name = name[0:99]

                # Transform the school type to the choice format expected in the model
                type = school["secteur_d_etablissement"]
                if type == "Public":
                    school_type = "public"
                elif type == "Privé":
                    school_type = "private"
                else:
                    school_type = None

                code = school["uai"]

                # Create a school object with the data and using the address and link
                # objects as FKs
                School.objects.create(
                    UAI_code=code,
                    name=name,
                    school_url=link,
                    # No current descriptions, use dummy text
                    description="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis luctus, diam quis venenatis laoreet, dolor nunc molestie quam, eget mattis mi dui eu nisi. Fusce lacinia metus nec sapien convallis, at tempor dui rutrum. Sed ac tincidunt sem, vitae malesuada mauris. Curabitur laoreet nulla aliquam tellus egestas accumsan. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Sed vehicula vestibulum mi, sed euismod metus luctus sed. Integer sed orci at massa ullamcorper sagittis. Morbi et viverra arcu.",
                    address=address,
                    school_type=type,
                )

        self.stdout.write(self.style.SUCCESS("Data has been imported successfully"))
