# Third-party imports
from rest_framework import serializers, viewsets
from django_filters import rest_framework as filters


# Local imports
from private_app.models import UserProfile, User
from .favorite import FavoriteSerializerPublic
from rest_framework import permissions


class UserSerializerPublic(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]


class UserProfileFilterPublic(filters.FilterSet):
    class Meta:
        model = UserProfile
        fields = {
            "user__first_name": ["icontains"],
            "user__last_name": ["icontains", "exact"],
            "about_me": ["icontains"],
            "student_at__name": ["icontains"],
            "student_at__cod_aff_form": ["exact"],
        }


class UserProfileSerializerPublic(serializers.ModelSerializer):
    user_extended = UserSerializerPublic(source="user", read_only=False)
    favorites_extended = FavoriteSerializerPublic(source="user.favorites", many=True)

    class Meta:
        model = UserProfile
        read_only_fields = [
            "user_extended",
            "user",
            "image_profile",
            "url_tiktok",
            "url_instagram",
            "about_me",
            "student_at",
            "favorites_extended",
        ]

        fields = [
            "user_extended",
            "user",
            "image_profile",
            "url_tiktok",
            "url_instagram",
            "about_me",
            "student_at",
            "favorites_extended",
        ]


class UserProfileViewSetPublic(viewsets.ReadOnlyModelViewSet):
    queryset = UserProfile.objects.all().filter(is_public=True)
    serializer_class = UserProfileSerializerPublic
    filterset_class = UserProfileFilterPublic
    filter_backends = (filters.DjangoFilterBackend,)
