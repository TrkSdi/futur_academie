from django.core.management.base import BaseCommand, CommandError
from private_app.models import (
    Address,
    Favorite,
    Link,
    School,
    StudyProgram,
    User,
    UserProfile,
)
from django.db import transaction
import random


class Command(BaseCommand):
    help = "Importing data for solo project"

    @transaction.atomic
    def handle(self, *args, **options):
        addresses = []
        for i in range(1, 6):
            address = Address.objects.create(
                street_address=f"{i} rue de Test",
                postcode=99 + i * 100 + i * 10 + i,
                locality="Testville",
            )
            addresses.append(address)
        schools = []
        for i in range(1, 6):
            if i % 2 == 0:
                school_type = "private"
            else:
                school_type = "public"
            school = School.objects.create(
                UAI_code="TEST000" + str(i),
                name="Test School " + str(i),
                school_url=Link.objects.create(
                    link_type="Autres", link_url=f"http://www.test-school{i}.fr"
                ),
                description="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis luctus, diam quis venenatis laoreet,\
                    dolor nunc molestie quam, eget mattis mi dui eu nisi. Fusce lacinia metus nec sapien convallis, at tempor\
                        dui rutrum. Sed ac tincidunt sem, vitae malesuada mauris. Curabitur laoreet nulla aliquam tellus \
                            egestas accumsan. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis \
                                egestas. Sed vehicula vestibulum mi, sed euismod metus luctus sed. Integer sed orci at massa \
                                    ullamcorper sagittis. Morbi et viverra arcu.",
                address=addresses[i - 1],
                school_type=school_type,
            )
            schools.append(school)
        programs = []
        discpline_types = [
            ("Droit_Sc_Politiques", "Droit Sc. politiques"),
            ("Economie_AES", "Économie, AES"),
            ("Arts_Lettres_Langues_SHS", "Arts, lettres, langues, SHS"),
            ("Sciences_Sante", "Sciences-santé"),
            ("STAPS", "STAPS"),
            ("Autres", "autres"),
        ]
        for i in range(0, len(schools)):
            j = 1
            for discipline_tuple in discpline_types:
                code = random.randint(1000, 9998) + j
                program = StudyProgram(
                    cod_aff_form=code,
                    name=f"Test Program {discipline_tuple[1]} {i}",
                    school=schools[i],
                    discipline=discipline_tuple[0],
                    url_parcoursup=Link.objects.create(
                        link_type="Autres", link_url=f"http://www.parcoursup.fr/{code}"
                    ),
                    acceptance_rate=round(random.randint(60, 90) / 2.1, 2),
                    L1_success_rate=round(random.randint(60, 90) / 2.1, 2),
                    insertion_rate=round(random.randint(60, 90) / 2.1, 2),
                    insertion_time_period=round(random.randint(60, 90) / 2.1, 2),
                    description="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis luctus, diam quis venenatis laoreet,\
                            dolor nunc molestie quam, eget mattis mi dui eu nisi. Fusce lacinia metus nec sapien convallis, at tempor\
                                dui rutrum. Sed ac tincidunt sem, vitae malesuada mauris. Curabitur laoreet nulla aliquam tellus \
                                    egestas accumsan. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis \
                                        egestas. Sed vehicula vestibulum mi, sed euismod metus luctus sed. Integer sed orci at massa \
                                            ullamcorper sagittis. Morbi et viverra arcu.",
                )
                j += 1
                programs.append(program)
        users = []
        for i in range(1, 6):
            user = User.objects.create(
                first_name=f"First{i}",
                last_name=f"Last{i}",
                email=f"user{i}@test.com",
                username=f"TestUser{i}",
            )
            users.append(user)
        for i in range(0, len(users)):
            if i % 2 == 0:
                public = True
            else:
                public = False
            UserProfile.objects.create(
                user=users[i],
                url_tiktok=Link.objects.create(
                    link_type="Twitter", link_url=f"http://www.twitter.com/TestUser{i}"
                ),
                url_instagram=Link.objects.create(
                    link_type="Instagram",
                    link_url=f"http://www.instagram.com/TestUser{i}",
                ),
                about_me="Lorem ipsum dolor sit amet, consectetur adipiscing elit. \
            Donec porttitor purus ligula, consequat feugiat leo ornare at. Vivamus \
                lacinia dapibus vestibulum. Vestibulum laoreet lectus risus, et \
                    mattis augue euismod a. Sed ac elit nisi. Phasellus iaculis \
                        interdum justo sit amet venenatis. Mauris tristique lectus \
                            vel rhoncus porttitor. Sed in nunc ante. Aliquam tempus \
                                posuere lacus.",
                is_public=public,
            )
        for user in users:
            i = 0
            while i < 3:
                program_number = random.randint(2, len(programs))
                if random.randint(0, 10) < 6:
                    note = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. \
                        Donec porttitor purus ligula, consequat feugiat leo ornare at. Vivamus \
                        lacinia dapibus vestibulum."
                else:
                    note = None
                Favorite.objects.create(
                    user=user,
                    study_program=programs[program_number - 1],
                    note=note,
                    status="applied",
                )
                i += 1

        self.stdout.write(self.style.SUCCESS("Data has been imported successfully"))
