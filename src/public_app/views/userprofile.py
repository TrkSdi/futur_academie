# Third-party imports
from rest_framework import serializers, viewsets
from django_filters import rest_framework as filters
from rest_framework import permissions


# Local imports
from private_app.models import UserProfile, User
from .favorite import FavoriteSerializerPublic
from .link import LinkSerializerPublic


class UserSerializerPublic(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name"]
        read_only_fields = ["first_name", "last_name"]


class UserProfileFilterPublic(filters.FilterSet):
    liked_study_program = filters.CharFilter(method='filter_by_liked_study_program')
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
        return queryset.filter(
            user__favorites__study_program__cod_aff_form=value
        )



class UserProfileSerializerPublic(serializers.ModelSerializer):
    user_extended = UserSerializerPublic(source="user", read_only=False)
    favorites_extended = FavoriteSerializerPublic(
        source="user.favorites", many=True)
    url_tiktok_extended = LinkSerializerPublic(source="url_tiktok")
    url_instagram_extended = LinkSerializerPublic(source="url_instagram")

    class Meta:
        model = UserProfile
        read_only_fields = [
            "user_extended",
            "image_profile",
            "url_tiktok",
            "url_instagram",
            "about_me",
            "student_at",
            "favorites_extended",
            "url_tiktok_extended",
            "url_instagram_extended",
        ]

        fields = [
            "user_extended",
            "image_profile",
            "url_tiktok",
            "url_instagram",
            "about_me",
            "student_at",
            "favorites_extended",
            "url_tiktok_extended",
            "url_instagram_extended",
        ]
        

class UserProfileViewSetPublic(viewsets.ReadOnlyModelViewSet):
    
    queryset = UserProfile.objects.all().filter(is_public=True)
    serializer_class = UserProfileSerializerPublic
    filterset_class = UserProfileFilterPublic
    filter_backends = (filters.DjangoFilterBackend,)
    permission_classes = [permissions.AllowAny]
