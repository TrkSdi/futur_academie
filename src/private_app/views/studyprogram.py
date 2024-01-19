# Third-party imports
from django_filters import rest_framework as filters
from rest_framework import serializers, viewsets
from rest_framework import permissions

# Local imports
from private_app.models import StudyProgram


class StudyProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyProgram
        fields = [
            "cod_aff_form",
            "name",
            "school",
            "discipline",
            "url_parcoursup",
            "acceptance_rate",
            "L1_success_rate",
            "insertion_rate",
            "insertion_time_period",
            "description",
        ]


class StudyProgramFilter(filters.FilterSet):
    class Meta:
        model = StudyProgram
        fields = {
            "cod_aff_form": ["exact"],
            "name": ["icontains", "exact"],
            "school": ["exact"],
            "url_parcoursup": ["exact"],
            "acceptance_rate": ["gt", "lt"],
            "L1_success_rate": ["gt", "lt"],
            "description": ["icontains"],
            "diploma_earned_ontime": ["gt", "lt"],
            "available_places": ["gt", "lt"],
            "number_applicants": ["gt", "lt"],
            "percent_scholarship": ["gt", "lt"],
        }


class StudyProgramViewSet(viewsets.ModelViewSet):
    queryset = StudyProgram.objects.all()
    serializer_class = StudyProgramSerializer
    filterset_class = StudyProgramFilter
    filter_backends = [
        filters.DjangoFilterBackend,
    ]
    permission_classes = [permissions.IsAdminUser]
