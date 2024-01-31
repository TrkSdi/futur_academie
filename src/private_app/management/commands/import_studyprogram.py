# Standard library imports
import json

# Third-party imports
from django.contrib.gis.geos import Point
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

# Local imports
from private_app.models import Address, Link, School, StudyProgram


def get_quartile(number, stats):
    if not isinstance(number, float):
        return None
    elif number <= stats[0]:
        return "Q1"
    elif number <= stats[1]:
        return "Q2"
    elif number <= stats[2]:
        return "Q3"
    else:
        return "Q4"


class Command(BaseCommand):
    help = "Importing data for studyProgram information"

    @transaction.atomic
    def handle(self, *args, **options):
        # file_path = "./study_program_data.json"
        file_path = r"./src/private_app/management/commands/study_program_data.json"

        # column#0.25#0.5#0.75
        PERCENT_ADMITTED_QS = [37.0, 60.0, 87.0]
        DIPLOMA_EARNED_ONTIME_QS = [47.6, 58.7, 66.8]
        PERCENT_SCHOLARSHIP_QS = [12.0, 17.0, 23.0]
        L2_CONTINUATION_RATE = [43.6, 82.3, 85.3]

        with open(file_path, "r") as f:
            data = json.load(f)
            total_programs = len(data)
            for index, program_data in enumerate(data):
                if index % 100 == 0:
                    complete = index / total_programs * 100
                    print(f"Import is {complete}% completed.")
                try:
                    # Récupère l'objet School basé sur le code UAI
                    school = School.objects.get(UAI_code=program_data["cod_uai"])
                except School.DoesNotExist:
                    locality = program_data["city"]
                    school_address = Address.objects.create(locality=locality)
                    school_uai = program_data["cod_uai"]
                    if program_data["school_type"] == "Public":
                        type = "public"
                    else:
                        type = "private"
                    school_name = program_data["school_name"]
                    link = Link.objects.create(
                        link_type="SchoolWebsite", link_url="nonsense.com"
                    )
                    school = School.objects.create(
                        UAI_code=school_uai,
                        name=school_name,
                        description="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis luctus, diam quis venenatis laoreet, dolor nunc molestie quam, eget mattis mi dui eu nisi. Fusce lacinia metus nec sapien convallis, at tempor dui rutrum. Sed ac tincidunt sem, vitae malesuada mauris. Curabitur laoreet nulla aliquam tellus egestas accumsan. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Sed vehicula vestibulum mi, sed euismod metus luctus sed. Integer sed orci at massa ullamcorper sagittis. Morbi et viverra arcu.",
                        address=school_address,
                        school_url=link,
                        school_type=type,
                    )

                # Création d'un objet Link pour la page Parcoursup du programme variable url
                url = (
                    "https://dossier.parcoursup.fr/Candidats/public/fiches/afficherFicheFormation?g_ta_cod="
                    + str(program_data["cod_aff_form"])
                )
                url_parcoursup = Link.objects.create(
                    link_type="Parcoursup", link_url=url
                )

                longitude = program_data["geolocation"]["lon"]
                latitude = program_data["geolocation"]["lat"]
                # Create the point object with the GPS position
                coordinates = Point(x=longitude, y=latitude, srid=4326)
                address = Address.objects.create(
                    locality=program_data["city"], geolocation=coordinates
                )
                if program_data["selectivity"] == "formation sélective":
                    selectivity = True
                else:
                    selectivity = False

                if program_data["description"]:
                    description = program_data["description"][0:250]
                else:
                    description = None

                if program_data["job_prospects"]:
                    job_prospects = program_data["job_prospects"][0:250]
                else:
                    job_prospects = None
                # Création de l'objet StudyProgram
                StudyProgram.objects.create(
                    cod_aff_form=int(program_data["cod_aff_form"]),
                    name="test",  # program_data["program_name"],
                    is_selective=selectivity,
                    address=address,
                    school=school,
                    url_parcoursup=url_parcoursup,
                    acceptance_rate=program_data["percent_admitted"],
                    available_places=program_data["available_places"],
                    number_applicants=program_data["number_applicants"],
                    percent_scholarship=program_data["percent_scholarship"],
                    out_of_sector_candidates=program_data["out_of_sector_candidates"],
                    diploma_earned_ontime=program_data["diploma_earned_ontime"],
                    acceptance_rate_quartile=get_quartile(
                        program_data["percent_admitted"], PERCENT_ADMITTED_QS
                    ),
                    L1_success_rate_quartile=get_quartile(
                        program_data["L2_continuation_rate"], L2_CONTINUATION_RATE
                    ),
                    diploma_earned_ontime_quartile=get_quartile(
                        program_data["diploma_earned_ontime"], DIPLOMA_EARNED_ONTIME_QS
                    ),
                    percent_scholarship_quartile=get_quartile(
                        program_data["percent_scholarship"], PERCENT_SCHOLARSHIP_QS
                    ),
                    description=description,
                    job_prospects=job_prospects,
                )

        self.stdout.write(
            self.style.SUCCESS("Study program data has been imported successfully")
        )
