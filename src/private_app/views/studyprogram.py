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
            "url_parcoursup",
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
            "acceptance_rate_quartile": ["gt", "lt"],
            "L1_success_rate_quartile": ["gt", "lt"],
            "diploma_earned_ontime_quartile": ["gt", "lt"],
            "percent_scholarship_quartile": ["gt", "lt"],
            "job_prospects": ["gt", "lt"],
        }


class StudyProgramViewSet(viewsets.ModelViewSet):
    queryset = StudyProgram.objects.all()
    serializer_class = StudyProgramSerializer
    filterset_class = StudyProgramFilter
    filter_backends = [
        filters.DjangoFilterBackend,
    ]
    permission_classes = [permissions.IsAdminUser]
