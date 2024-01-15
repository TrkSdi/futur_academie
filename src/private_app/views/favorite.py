# Third-party imports
from rest_framework import serializers, viewsets
from django_filters import rest_framework as filters

# Local imports
from private_app.models import Favorite


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        read_only_fields = ("id",)

        fields = ["id", "user", "study_program", "note", "status"]

class FavoriteFilter(filters.FilterSet):
    # add possibility to filter by address
    class Meta:
        model = Favorite
        fields = {
            "UAI_code": ["exact"],
            "name": ["icontains", "exact"],
            "description": ["icontains"],
            "school_type": ["exact"],
        }

class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    filterset_class = FavoriteFilter
    filter_backends = [
        filters.DjangoFilterBackend,
    ]
    

