# Third-party imports
from django_filters import rest_framework as filters
from rest_framework import serializers, viewsets
from rest_framework import permissions

# Local imports
from private_app.models import StudyProgram
from .link import LinkSerializerPublic


class StudyProgramSerializerPublic(serializers.ModelSerializer):
    url_parcoursup_extended = LinkSerializerPublic(source="url_parcoursup")

    class Meta:
        model = StudyProgram
        fields = [
            "cod_aff_form",
            "name",
            "school",
            "discipline",
            "url_parcoursup",
            "url_parcoursup_extended",
            "acceptance_rate",
            "L1_success_rate",
            "insertion_rate",
            "insertion_time_period",
            "description",
        ]
        read_only_fields = [
            "cod_aff_form",
            "name",
            "school",
            "discipline",
            "url_parcoursup",
            "url_parcoursup_extended",
            "acceptance_rate",
            "L1_success_rate",
            "insertion_rate",
            "insertion_time_period",
            "description",
        ]


class StudyProgramFilterPublic(filters.FilterSet):
    class Meta:
        model = StudyProgram
        fields = {
            "cod_aff_form": ["exact"],
            "name": ["icontains", "exact"],
            "school": ["exact"],
            "discipline": ["exact"],
            "url_parcoursup": ["exact"],
            "acceptance_rate": ["exact", "gt", "lt"],
            "L1_success_rate": ["exact", "gt", "lt"],
            "insertion_rate": ["exact", "gt", "lt"],
            "insertion_time_period": ["icontains"],
            "description": ["icontains"],
        }


class StudyProgramViewSetPublic(viewsets.ReadOnlyModelViewSet):
    queryset = StudyProgram.objects.all()
    serializer_class = StudyProgramSerializerPublic
    filterset_class = StudyProgramFilterPublic
    filter_backends = [
        filters.DjangoFilterBackend,
    ]
