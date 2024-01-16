# Third-party imports
from rest_framework import serializers, viewsets
from django_filters import rest_framework as filters
from rest_framework import permissions
from django.db.models import Q

# Local imports
from private_app.models import Favorite

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        read_only_fields = ("id",)
        fields = [
            "id",
            "user",
            "study_program",
            "note",
            "status",
        ]


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
    serializer_class = FavoriteSerializer
    filterset_class = FavoriteFilter
    filter_backends = [
        filters.DjangoFilterBackend,
    ]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        """Return the queryset with only favorites owned by the user requesting them"""
        if self.request.user.is_superuser:
            queryset = Favorite.objects.all()
        else:
            queryset = Favorite.objects.all().filter(user=self.request.user)
        return queryset
