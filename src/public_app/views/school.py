# Third-party imports
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django_filters import rest_framework as filters
from rest_framework import serializers, viewsets
from rest_framework import permissions

# Local imports
from private_app.models import School
from .address import AddressSerializerPublic
from .link import LinkSerializerPublic


class SchoolSerializerPublic(serializers.ModelSerializer):
    address_extended = AddressSerializerPublic(source="address")
    school_url_extended = LinkSerializerPublic(source="school_url")

    class Meta:
        model = School
        fields = [
            "UAI_code",
            "name",
            "school_url",
            "school_url_extended",
            "description",
            "address",
            "address_extended",
            "school_type",
        ]
        read_only_fields = [
            "UAI_code",
            "name",
            "school_url",
            "school_url_extended",
            "description",
            "address",
            "address_extended",
            "school_type",
        ]


class SchoolFilterPublic(filters.FilterSet):
    # Returns all results ordered by distance from the point given in format long,lat
    distance__from = filters.CharFilter(method="filter_by_distance")
    # Returns all results within the radius in km of the point given in format long,lat,radius
    distance__lte = filters.CharFilter(method="filter_distance_lte")

    class Meta:
        model = School
        fields = {
            "UAI_code": ["exact"],
            "name": ["icontains", "exact"],
            "description": ["icontains"],
            "school_type": ["exact"],
            "address__postcode": ["icontains"],
            "address__locality": ["icontains"],
        }

    def filter_by_distance(self, queryset, name, value):
        """This function accepts a value string of format long,lat. It returns a
        queryset of all matching schools ordered by the closest distance to the
        provided geolocation.

        Returns:
            queryset: all matching schools ordered by distance
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
        given in kilometers. It returns a queryset of all matching schools within the given
        perimeter.

        Returns:
            queryset: all matching schools ordered by distance
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


class SchoolViewSetPublic(viewsets.ReadOnlyModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializerPublic
    filterset_class = SchoolFilterPublic
    filter_backends = [
        filters.DjangoFilterBackend,
    ]
    permission_classes = [permissions.AllowAny]
