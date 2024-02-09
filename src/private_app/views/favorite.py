# Third-party imports
from rest_framework import serializers, viewsets
from django_filters import rest_framework as filters
import jwt
from django.conf import settings

from datetime import datetime, timedelta
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response

# Local imports
from private_app.models import Favorite
from . import StudyProgramReducedSerializer


class FavoriteSerializer(serializers.ModelSerializer):
    study_program_extended = StudyProgramReducedSerializer(
        source="study_program", read_only=True
    )

    class Meta:
        model = Favorite
        read_only_fields = ("id", "study_program_extended")
        fields = [
            "id",
            "user",
            "study_program",
            "note",
            "status",
            "study_program_extended",
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

    @action(detail=False, methods=["GET"])
    def share_favorites(self, request):
        expiration_time = datetime.utcnow() + timedelta(days=14)
        user_id = request.user.id.hex
        payload = {
            "user_id": user_id,
            "exp": expiration_time,
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
        # url = f"{settings.ROOT_IP}/API_public/favorite/view_shared/?list={token}"
        response = {"token": token, "exp": expiration_time}
        return Response(response)
