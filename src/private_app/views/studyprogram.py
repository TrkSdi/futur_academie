# Third-party imports
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django_filters import rest_framework as filters
from rest_framework import serializers, viewsets
from rest_framework import permissions

# Local imports
from private_app.models import StudyProgram
from .address import AddressSerializer
from .link import LinkSerializer


class StudyProgramSerializer(serializers.ModelSerializer):
    address_extended = AddressSerializer(source="address")
    url_parcoursup_extended = LinkSerializer(source="url_parcoursup")

    class Meta:
        model = StudyProgram
        fields = [
            "cod_aff_form",
            "name",
            "school",
            "address",
            "address_extended",
            "url_parcoursup",
            "url_parcoursup_extended",
            "acceptance_rate",
            "L1_success_rate",
            "description",
            "diploma_earned_ontime",
            "available_places",
            "number_applicants",
            "percent_scholarship",
            "acceptance_rate_quartile",
            "L1_success_rate_quartile",
            "diploma_earned_ontime_quartile",
            "percent_scholarship_quartile",
            "job_prospects",
        ]


class StudyProgramFilter(filters.FilterSet):
    # Returns all results ordered by distance from the point given in format long,lat
    distance__from = filters.CharFilter(method="filter_by_distance")
    # Returns all results within the radius in km of the point given in format long,lat,radius
    distance__lte = filters.CharFilter(method="filter_distance_lte")

    class Meta:
        model = StudyProgram
        fields = {
            "cod_aff_form": ["exact"],
            "name": ["icontains", "exact"],
            "school": ["exact"],
            "address__locality": ["icontains", "exact"],
            "url_parcoursup": ["exact"],
            "acceptance_rate": ["gt", "lt"],
            "L1_success_rate": ["gt", "lt"],
            "description": ["icontains"],
            "diploma_earned_ontime": ["gt", "lt"],
            "available_places": ["gt", "lt"],
            "number_applicants": ["gt", "lt"],
            "percent_scholarship": ["gt", "lt"],
            "acceptance_rate_quartile": ["gt", "lt"],
            "L1_success_rate_quartile": ["gt", "lt"],
            "diploma_earned_ontime_quartile": ["gt", "lt"],
            "percent_scholarship_quartile": ["gt", "lt"],
            "job_prospects": ["gt", "lt"],
        }

    def filter_by_distance(self, queryset, name, value):
        """This function accepts a value string of format long,lat. It returns a
        queryset of all matching study programms ordered by the closest distance to the
        provided geolocation.

        Returns:
            queryset: all matching study programms ordered by distance
        """
        location = value.split(",")
        long = float(location[0])
        lat = float(location[1])
        geo_loc = Point(x=long, y=lat, srid=4326)
        return queryset.annotate(
            distance=Distance("address__geolocation", geo_loc)
        ).order_by("distance")

    def filter_distance_lte(self, queryset, name, value):
        """This function accepts a value string of format long,lat,radius with the radius
        given in kilometers. It returns a queryset of all matching study programms within the given
        perimeter.

        Returns:
            queryset: all matching study programms ordered by distance
        """
        location = value.split(",")
        long = float(location[0])
        lat = float(location[1])
        radius = float(location[2]) * 1000
        geo_loc = Point(x=long, y=lat, srid=4326)
        return (
            queryset.annotate(distance=Distance("address__geolocation", geo_loc))
            .filter(distance__lte=radius)
            .order_by("distance")
        )


class StudyProgramViewSet(viewsets.ModelViewSet):
    queryset = StudyProgram.objects.all()
    serializer_class = StudyProgramSerializer
    filterset_class = StudyProgramFilter
    filter_backends = [
        filters.DjangoFilterBackend,
    ]
    permission_classes = [permissions.IsAdminUser]
