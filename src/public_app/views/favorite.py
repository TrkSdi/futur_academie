# Third-party imports
from rest_framework import serializers, viewsets
from django_filters import rest_framework as filters
from rest_framework import permissions
from rest_framework.decorators import action
import jwt
from django.http import JsonResponse
from django.conf import settings
from rest_framework.response import Response

# Local imports
from private_app.models import Favorite
from .studyprogram import StudyProgramSerializerPublic


class FavoriteSerializerPublic(serializers.ModelSerializer):
    study_program_extended = StudyProgramSerializerPublic(
        source="study_program", read_only=True
    )

    class Meta:
        model = Favorite
        read_only_fields = (
            "id",
            "user",
            "study_program",
            "note",
            "status",
            "study_program_extended",
        )
        fields = [
            "id",
            "user",
            "study_program",
            "note",
            "status",
            "study_program_extended",
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
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=["GET"])
    def view_shared(self, request):
        token = request.GET.get("list")
        if token[-1] == "/":
            token = token[:-1]
        token = bytes(token, "utf-8")
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("user_id")
            queryset = Favorite.objects.filter(user_id=user_id)
            response = FavoriteSerializerPublic(queryset, many=True).data
            return Response(response)
        except jwt.ExpiredSignatureError:
            return JsonResponse({"message": "Token has expired"}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({"message": "Invalid token"}, status=401)
