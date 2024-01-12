# Third-party imports
from django_filters import rest_framework as filters
from rest_framework import serializers, viewsets

# Local imports
from private_app.models import School


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = [
            "UAI_code",
            "name",
            "school_url",
            "description",
            "address",
            "school_type",
        ]


class SchoolFilter(filters.FilterSet):
    # add possibility to filter by address
    class Meta:
        model = School
        fields = {
            "UAI_code": ["exact"],
            "name": ["icontains", "exact"],
            "description": ["icontains"],
            "school_type": ["exact"],
        }


class SchoolViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    filterset_class = SchoolFilter
    filter_backends = [
        filters.DjangoFilterBackend,
    ]
