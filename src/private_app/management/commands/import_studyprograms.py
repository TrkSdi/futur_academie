# Standard library imports
import json

# Third-party imports
from django.contrib.gis.geos import Point
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

# Local imports
from private_app.models import Address, Link, School, StudyProgram


def get_quartile(number: float, stats: list[float]) -> str:
    """Takes a statistic and a list of the quartile cut-off points for the type of statistic
    and returns a string indicating which quartile from Q1 (bottom 25%) to Q4 (top 25%) the
    statistic falls in.

    Args:
        number (float): the given statistic for the study program
        stats (list[float]): the array of quartile points for the type of statistic given

    Returns:
        str: a two-character string representing the quartile
    """
    if not isinstance(number, float):
        return ""
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
        file_path: str = (
            r"./src/private_app/management/commands/study_program_data.json"
        )

        # Each column represents a qaurtile cut-off point #0.25#0.5#0.75
        PERCENT_ADMITTED_QS: list[float] = [37.0, 60.0, 87.0]
        DIPLOMA_EARNED_ONTIME_QS: list[float] = [47.6, 58.7, 66.8]
        PERCENT_SCHOLARSHIP_QS: list[float] = [12.0, 17.0, 23.0]
        L2_CONTINUATION_RATE: list[float] = [43.6, 82.3, 85.3]

        with open(file_path, "r") as f:
            data: list[dict] = json.load(f)
            total_programs: int = len(data)

            for index, program_data in enumerate(data):
                # Indicate progress in the terminal for each 100 programs imported
                if index % 100 == 0:
                    complete: float = index / total_programs * 100
                    print(f"Import is {complete}% completed.")
                try:
                    # Link the studyProgram object to its school based on the code UAI
                    school: School = School.objects.get(
                        UAI_code=program_data["cod_uai"]
                    )
                except School.DoesNotExist:
                    locality: str = program_data["city"]
                    school_address: Address = Address.objects.create(locality=locality)
                    school_uai: str = program_data["cod_uai"]
                    if program_data["school_type"] == "Public":
                        type: str = "public"
                    else:
                        type: str = "private"
                    school_name: str = program_data["school_name"]
                    school: School = School.objects.create(
                        UAI_code=school_uai,
                        name=school_name,
                        description="La déscription de cette établissement n'a pas encore été renseignée.",
                        address=school_address,
                        school_type=type,
                    )

                # Create a Link object for the program parcoursup page
                url: str = (
                    "https://dossier.parcoursup.fr/Candidats/public/fiches/afficherFicheFormation?g_ta_cod="
                    + str(program_data["cod_aff_form"])
                )
                url_parcoursup: Link = Link.objects.create(
                    link_type="Parcoursup", link_url=url
                )
                # Create an Address object for the program
                longitude: float = program_data["geolocation"]["lon"]
                latitude: float = program_data["geolocation"]["lat"]
                # SRID 4326 indicates the point object is a gps position
                coordinates: Point = Point(x=longitude, y=latitude, srid=4326)
                address: Address = Address.objects.create(
                    locality=program_data["city"], geolocation=coordinates
                )

                if program_data["selectivity"] == "formation sélective":
                    selectivity: bool = True
                else:
                    selectivity = False

                if program_data["description"]:
                    description: str = program_data["description"]
                else:
                    description = ""

                if program_data["job_prospects"]:
                    job_prospects: str = program_data["job_prospects"]
                else:
                    job_prospects = ""

                # Create the StudyProgram object
                StudyProgram.objects.create(
                    cod_aff_form=int(program_data["cod_aff_form"]),
                    name=program_data["program_name"],
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
