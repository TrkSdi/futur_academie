# Third-party imports
from django_filters import rest_framework as filters
from rest_framework import serializers, viewsets

# Local imports
from private_app.models import School
from .address import AddressSerializer
from .link import LinkSerializer


class SchoolSerializer(serializers.ModelSerializer):
    address_extended = AddressSerializer(source="address")
    school_url_extended = LinkSerializer(source="school_url")

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


class SchoolFilter(filters.FilterSet):
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


class SchoolViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    filterset_class = SchoolFilter
    filter_backends = [
        filters.DjangoFilterBackend,
    ]
