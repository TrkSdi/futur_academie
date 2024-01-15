# Third-party imports
from rest_framework import serializers, viewsets
from django_filters import rest_framework as filters

# Local imports
from private_app.models import Favorite


class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favorite
        read_only_fields = ("id",)
        fields = ["id", "user", "study_program",
                  "note", "status", "user_extended"]


class FavoriteFilter(filters.FilterSet):
    class Meta:
        model = Favorite
        fields = {
            "user__username": ["icontains"],
            "user__first_name": ["icontains"],
            "user__last_name": ["icontains"],
            "study_program": ["exact"],
            "note": ["icontains"],
            "status": ["exact"],
        }


class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    filterset_class = FavoriteFilter
    filter_backends = [
        filters.DjangoFilterBackend,
    ]
