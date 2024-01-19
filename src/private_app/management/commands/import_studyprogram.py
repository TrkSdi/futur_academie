
        
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
    StudyProgram
)


class Command(BaseCommand):
    help = "Importing data for studyProgram information"

    @transaction.atomic
    def handle(self, *args, **options):
        # file_path = "./study_program_data.json"
        file_path = r"C:\Users\Strike\Documents\Diginamic_Cours\Fil_Rouge\futur_academie\src\private_app\management\commands\study_program_data.json"

        with open(file_path, "r") as f:
            data = json.load(f)
    
            for program_data in data:
                try:
                    # Récupère l'objet School basé sur le code UAI
                    school = School.objects.get(UAI_code=program_data["cod_uai"])
                except School.DoesNotExist:
                    # Si aucune école avec ce code UAI n'est trouvée, le programme est ignoré
                    self.stdout.write(self.style.WARNING(f"School with UAI code {school} not found. Skipping program."))
                    continue

                # Création d'un objet Link pour la page Parcoursup du programme variable url
                url="https://dossier.parcoursup.fr/Candidats/public/fiches/afficherFicheFormation?g_ta_cod="+ str(program_data["cod_aff_form"])
                url_parcoursup = Link.objects.create(link_type="Parcoursup", link_url=url)
                
                longitude = program_data["geolocation"]["lon"]
                latitude = program_data["geolocation"]["lat"]
                # Create the point object with the GPS position
                coordinates = Point(x=longitude, y=latitude, srid=4326)
                address= Address.objects.create(locality=program_data["city"],geolocation=coordinates)
                
                    
                # Création de l'objet StudyProgram
                StudyProgram.objects.create(
                    cod_aff_form=int(program_data["cod_aff_form"]),
                    name=program_data["program_name"],
                    is_selective=bool(program_data["selectivity"]),
                    address=address,
                    school=school,
                    url_parcoursup=url_parcoursup,
                    acceptance_rate=program_data["percent_admitted"],
                    available_places=program_data["available_places"],
                    number_applicants=program_data["number_applicants"],
                    percent_scholarship=program_data["percent_scholarship"],
                    out_of_sector_candidates=program_data["out_of_sector_candidates"],
                    diploma_earned_ontime=program_data["diploma_earned_ontime"],
                    # acceptance_rate_quartile=program_data["NOM_COLONNE"],
                    # L1_success_rate_quartile=program_data["NOM_COLONNE"],
                    # diploma_earned_ontime_quartile=program_data["NOM_COLONNE"],
                    # percent_scholarship_quartile=program_data["NOM_COLONNEe"],
                    description=program_data["description"],
                    job_prospects=program_data["job_prospects"],
                )
                   

        self.stdout.write(self.style.SUCCESS("Study program data has been imported successfully"))