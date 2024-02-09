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
        # Different systems require file path to be slightly different
        # file_path: str = r"./fr-esr-principaux-etablissements-enseignement-superieur.json"
        file_path: str = (
            r"./src/private_app/management/commands/fr-esr-principaux-etablissements-enseignement-superieur.json"
        )

        with open(file_path, "r") as f:
            # Load the data
            data: list[dict] = json.load(f)
            # Loop through schools to ceate address, link and school objects for each
            for school in data:
                # If there is no UAI code, ignore the data
                if not school["uai"]:
                    break

                # Create an address object with the given data
                street_address: str = school["adresse_uai"]
                locality: str = school["localite_acheminement_uai"]
                postcode: str = school["code_postal_uai"]
                longitude: float = school["coordonnees"]["lon"]
                latitude: float = school["coordonnees"]["lat"]
                # Create the point object with the GPS position
                coordinates: Point = Point(x=longitude, y=latitude, srid=4326)

                address: Address = Address.objects.create(
                    street_address=street_address,
                    locality=locality,
                    postcode=postcode,
                    geolocation=coordinates,
                )

                # If the school has a url, make a link object for it
                if school["url"]:
                    website: str = school["url"]
                    link: Link | None = Link.objects.create(
                        link_type="SchoolWebsite", link_url=website
                    )
                else:
                    link = None

                name: str = school["uo_lib"]

                # Transform the school type to the choice format expected in the model
                type: str = school["secteur_d_etablissement"]
                if type == "Public":
                    school_type: str = "public"
                elif type == "Privé":
                    school_type = "private"
                else:
                    school_type = ""

                code: str = school["uai"]

                # Create a school object with the data and using the address and link
                # objects as FKs
                School.objects.create(
                    UAI_code=code,
                    name=name,
                    school_url=link,
                    # No current descriptions, use dummy text
                    description="Déscriptions des établissements à venir. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis luctus, diam quis venenatis laoreet, dolor nunc molestie quam, eget mattis mi dui eu nisi. Fusce lacinia metus nec sapien convallis, at tempor dui rutrum. Sed ac tincidunt sem, vitae malesuada mauris. Curabitur laoreet nulla aliquam tellus egestas accumsan. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Sed vehicula vestibulum mi, sed euismod metus luctus sed. Integer sed orci at massa ullamcorper sagittis. Morbi et viverra arcu.",
                    address=address,
                    school_type=type,
                )

        self.stdout.write(self.style.SUCCESS("Data has been imported successfully"))
