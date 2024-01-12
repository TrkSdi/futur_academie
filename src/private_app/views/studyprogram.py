# Third-party imports
from rest_framework import serializers, viewsets

# Local imports
from private_app.models import StudyProgram


class StudyProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyProgram
        fields = ["cod_aff_form",
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


class StudyProgramViewSet(viewsets.ModelViewSet):
    queryset = StudyProgram.objects.all()
    serializer_class = StudyProgramSerializer
