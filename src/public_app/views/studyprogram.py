# Third-party imports
from django.db.models import Q
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django_filters import rest_framework as filters
from rest_framework import serializers, viewsets
from rest_framework import permissions
from rest_framework.filters import OrderingFilter
from django.db.models import Case, When, Value, FloatField
from django.db.models import F


# Local imports
from private_app.models import StudyProgram
from .link import LinkSerializerPublic
from .school import SchoolSerializerPublicReduced
from private_app.views import AddressSerializer


class StudyProgramSerializerPublic(serializers.ModelSerializer):
    url_parcoursup_extended = LinkSerializerPublic(source="url_parcoursup")
    school_extended = SchoolSerializerPublicReduced(source="school")
    address_extended = AddressSerializer(source="address")

    class Meta:
        model = StudyProgram
        fields = [
            "cod_aff_form",

            "name",
            "school",
            "school_extended",
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
        read_only_fields = [
            "cod_aff_form",
            "name",
            "school",
            "school_extended",
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


class StudyProgramFilterPublic(filters.FilterSet):
    # Returns all results ordered by distance from the point given in format long,lat
    distance__from = filters.CharFilter(method="filter_by_distance")
    # Returns all results within the radius in km of the point given in format long,lat,radius
    distance__lte = filters.CharFilter(method="filter_distance_lte")

    search_all = filters.CharFilter(
        method="general_search",
        label="Search by program name, description, or job prospects at once.",
    )

    class Meta:
        model = StudyProgram
        fields = {
            "cod_aff_form": ["exact"],
            "name": ["icontains", "exact"],
            "school": ["exact"],
            "school__name": ["icontains"],
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

    def general_search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value)
            | Q(school__name__icontains=value)
            | Q(description__icontains=value)
            | Q(job_prospects__icontains=value)
        )

    def filter_distance_lte(self, queryset, name, value):
        """This function accepts a value string of format long,lat,radius with the radius
        given in kilometers. It returns a queryset of all matching study programms within the given
        perimeter.

        Returns:
            queryset: all matching study programms ordered by distance
        """
        try:
            long, lat, radius = map(float, value.split(','))
            radius_km = radius * 1000
            geo_loc = Point(long, lat, srid=4326)
            return queryset.annotate(
                distance=Distance("address__geolocation", geo_loc)
            ).filter(distance__lte=radius_km).order_by('distance')
        except (ValueError, TypeError):
            return queryset.none()


class NullsAlwaysLastOrderingFilter(OrderingFilter):
    def filter_queryset(self, request, queryset, view):
        ordering = self.get_ordering(request, queryset, view)
        if ordering:
            f_ordering = []
            for field in ordering:
                if field.startswith('-'):
                    field_name = field[1:]
                    f_ordering.append(F(field_name).desc(nulls_last=True))
                else:
                    f_ordering.append(F(field).asc(nulls_last=True))
            return queryset.order_by(*f_ordering)
        return queryset


class StudyProgramViewSetPublic(viewsets.ReadOnlyModelViewSet):

    queryset = StudyProgram.objects.all()
    serializer_class = StudyProgramSerializerPublic
    filterset_class = StudyProgramFilterPublic
    filter_backends = [filters.DjangoFilterBackend,
                       NullsAlwaysLastOrderingFilter]
# to have a filter "order by"
    ordering_fields = ['acceptance_rate',
                       'L1_success_rate', 'available_places', 'diploma_earned_ontime', 'number_applicants', 'percent_scholarship']
    permission_classes = [permissions.AllowAny]
