# Third-party imports
from rest_framework import serializers, viewsets
from django_filters import rest_framework as filters
from rest_framework import permissions
from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer


# Local imports
from private_app.models import UserProfile, User
from . import (
    FavoriteSerializerPublic,
    LinkSerializerPublic,
    SchoolReducedSerializerPublic,
)


class UserSerializerPublic(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name"]
        read_only_fields = ["first_name", "last_name"]


class UserProfileFilterPublic(filters.FilterSet):
    liked_study_program = filters.CharFilter(method="filter_by_liked_study_program")

    class Meta:
        model = UserProfile
        fields = {
            "user__first_name": ["icontains"],
            "user__last_name": ["icontains", "exact"],
            "about_me": ["icontains"],
            "student_at__name": ["icontains"],
            "student_at__cod_aff_form": ["exact"],
        }

    def filter_by_liked_study_program(self, queryset, name, value):
        return queryset.filter(user__favorites__study_program__cod_aff_form=value)


class UserProfileSerializerPublic(serializers.ModelSerializer):
    user_extended = UserSerializerPublic(source="user")
    favorites_extended = FavoriteSerializerPublic(source="user.favorites", many=True)
    url_tiktok_extended = LinkSerializerPublic(source="url_tiktok")
    url_instagram_extended = LinkSerializerPublic(source="url_instagram")
    student_at_extended = SchoolReducedSerializerPublic(source="student_at")

    class Meta:
        model = UserProfile
        read_only_fields = [
            "id",
            "user_extended",
            "user",
            "image_profile",
            "url_tiktok",
            "url_tiktok_extended",
            "url_instagram",
            "url_instagram_extended",
            "about_me",
            "is_public",
            "student_at",
            "student_at_extended",
            "favorites_extended",
        ]
        fields = [
            "id",
            "user_extended",
            "user",
            "image_profile",
            "url_tiktok",
            "url_tiktok_extended",
            "url_instagram",
            "url_instagram_extended",
            "about_me",
            "is_public",
            "student_at",
            "student_at_extended",
            "favorites_extended",
        ]


class UserProfileViewSetPublic(viewsets.ReadOnlyModelViewSet):

    queryset = UserProfile.objects.all().filter(is_public=True)
    serializer_class = UserProfileSerializerPublic
    filterset_class = UserProfileFilterPublic
    filter_backends = (filters.DjangoFilterBackend,)
    permission_classes = [permissions.AllowAny]


class CustomUserRegistrationSerializer(BaseUserRegistrationSerializer):
    class Meta(BaseUserRegistrationSerializer.Meta):
        fields = ("email", "password", "first_name", "last_name")
