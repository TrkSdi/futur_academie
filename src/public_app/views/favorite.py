# Third-party imports
from rest_framework import serializers, viewsets
from django_filters import rest_framework as filters
from rest_framework import permissions

# Local imports
from private_app.models import Favorite


class FavoriteSerializerPublic(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = [
            "user",
            "study_program",
            "status",
        ]
        read_only_fields = [
            "user",
            "study_program",
            "status",
        ]


class FavoriteFilterPublic(filters.FilterSet):
    class Meta:
        model = Favorite
        fields = {
            "user__username": ["icontains"],
            "user__first_name": ["icontains"],
            "user__last_name": ["icontains"],
            "study_program": ["exact"],
            "status": ["exact"],
        }


class FavoriteViewSetPublic(viewsets.ReadOnlyModelViewSet):
    queryset = Favorite.objects.all().filter(user__profile__is_public=True)
    serializer_class = FavoriteSerializerPublic
    filterset_class = FavoriteFilterPublic
    filter_backends = [
        filters.DjangoFilterBackend,
    ]
