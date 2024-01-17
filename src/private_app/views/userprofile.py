# Third-party imports
from rest_framework import serializers, viewsets
from django_filters import rest_framework as filters
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from rest_framework.decorators import action
from rest_framework.response import Response

# Local imports
from private_app.models import UserProfile, User
from .favorite import FavoriteSerializer
from rest_framework import permissions


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]


class UserProfileFilter(filters.FilterSet):
    class Meta:
        model = UserProfile
        fields = {
            "user__first_name": ["icontains"],
            "user__last_name": ["icontains", "exact"],
            "about_me": ["icontains"],
            "student_at__name": ["icontains"],
            "student_at__cod_aff_form": ["exact"],
        }


class UserProfileSerializer(serializers.ModelSerializer):
    user_extended = UserSerializer(source="user", read_only=False)
    favorites_extended = FavoriteSerializer(source="user.favorites", many=True)

    class Meta:
        model = UserProfile
        read_only_fields = ("id",)
        fields = [
            "id",
            "user_extended",
            "user",
            "image_profile",
            "url_tiktok",
            "url_instagram",
            "about_me",
            "is_public",
            "student_at",
            "favorites_extended",
        ]


class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    filterset_class = UserProfileFilter
    filter_backends = (filters.DjangoFilterBackend,)
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        """Return the queryset with only favorites owned by the user requesting them"""
        if self.request.user.is_superuser:
            queryset = UserProfile.objects.all()
        else:
            queryset = UserProfile.objects.all().filter(user=self.request.user)
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
        response = {
            "temporary_url": f"http://127.0.0.1:8000/API_public/favorite/view_shared/?list={token}"
        }
        return Response(response)
