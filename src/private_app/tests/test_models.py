# Third-party imports
from django.test import TestCase
from django.contrib.gis.geos import Point

# Local imports
from private_app.models import (
    Address,
    Favorite,
    Link,
    School,
    StudyProgram,
    User,
    UserProfile,
)


class ModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create an address
        coordinates = Point(47.09624640173994, -1.6599277027341754)
        address = Address.objects.create(
            street_address="1 rue de Test",
            postcode=44000,
            locality="Testville",
            geolocation=coordinates,
        )

        # Create a school website link longer than 30char
        link = Link.objects.create(
            link_type="SchoolWebsite", link_url="http://www.testing.com/123aaaaaaaaaa"
        )

        # Create a school with the above address and link
        school = School.objects.create(
            name="Test University",
            school_url=link,
            description="Test University was founded in Testville in 3023 to provide a well-rounded testing education to aspiring testers",
            address=address,
            school_type="private",
        )

        # Create a study program at the above school
        program = StudyProgram.objects.create(
            cod_aff_form=123456,
            name="Django and Angular Testing Studies",
            school=school,
            discipline="Sciences_Sante",
            url_parcoursup=Link.objects.create(
                link_type="ParcoursSupliink",
                link_url="https://dossier.parcoursup.fr/Candidats/public/fiches/afficherFicheFormation?g_ta_cod=123456",
            ),
            acceptance_rate="73.2",
            L1_success_rate="37.7",
            insertion_rate="64.8",
            insertion_time_period=12,
            description="Learn to test Djangular applications like the best!",
        )

        # Create a user
        user = User.objects.create(
            first_name="Ted",
            last_name="Testerton",
            username="TedTest",
            email="ted@test.com",
            password="Testing123!",
        )

        # Create a user profile set to private by default and no student_at attribute
        profile = UserProfile.objects.create(
            user=user,
            url_tiktok=Link.objects.create(
                link_type="Tiktok",
                link_url="http://www.tiktok.com/user/TedTestington123",
            ),
            url_instagram=Link.objects.create(
                link_type="Instagram",
                link_url="http://www.instagram.com/user/TedTestington123",
            ),
            about_me="I'm Ted Testerton and I am looking for a great study program.",
        )

        # Create a favorite with the user and program created above
        favorite = Favorite.objects.create(
            user=user,
            study_program=program,
            note="This program looks like one to test!",
            status="interested",
        )

    # TEST ADDRESS MODEL
    def test_max_length_street_address(self):
        address_object = Address.objects.first()
        max_length = address_object._meta.get_field("street_address").max_length
        self.assertEqual(max_length, 100)

    def test_max_length_locality(self):
        address_object = Address.objects.first()
        max_length = address_object._meta.get_field("locality").max_length
        self.assertEqual(max_length, 100)

    def test_address_label(self):
        address_object = Address.objects.first()
        field_label = address_object._meta.verbose_name_plural
        self.assertEqual(field_label, "Addresses")

    def test_address_object_name(self):
        address_object = Address.objects.first()
        expected_string = f"{address_object.locality}, {address_object.postcode}, {address_object.street_address}"
        self.assertEqual(str(address_object), expected_string)

    # TEST FAVORITE MODEL
    def test_max_length_favorite_note(self):
        favorite_object = Favorite.objects.first()
        max_length = favorite_object._meta.get_field("note").max_length
        self.assertEqual(max_length, 300)

    # TEST LINK MODEL
    def test_link_object_name(self):
        link_object = Link.objects.get(link_type="SchoolWebsite")
        url = link_object.link_url
        expected_result = f"SchoolWebsite : {url[:30]}..."
        self.assertEqual(str(link_object), expected_result)

    def test_link_url_max_length(self):
        link_object = Link.objects.first()
        max_length = link_object._meta.get_field("link_url").max_length
        self.assertEqual(max_length, 100)

    # TEST SCHOOL MODEL
    def test_school_name_max_length(self):
        school_object = School.objects.first()
        max_length = school_object._meta.get_field("name").max_length
        self.assertEqual(max_length, 100)

    def test_school_object_name(self):
        school_object = School.objects.first()
        name = school_object.name
        self.assertEqual(str(school_object), name)

    # TEST USERPROFILE MODEL
    def test_about_me_max_length(self):
        profile_object = UserProfile.objects.first()
        max_length = profile_object._meta.get_field("about_me").max_length
        self.assertEqual(max_length, 400)
