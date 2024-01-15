# Third-party imports
from rest_framework import serializers, viewsets
from django_filters import rest_framework as filters


# Local imports
from private_app.models import UserProfile, User
from .favorite import FavoriteSerializer
from rest_framework import permissions


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]


class UserProfileFilter(filters.FilterSet):
    # user_first_name = filters.CharFilter(
    #     field_name="first_name", lookup_expr="icontains"
    # )

    class Meta:
        model = UserProfile
        fields = {"user__first_name": ["icontains"],
                  "user__last_name": ["icontains", "exact"],
                  "about_me": ["icontains"],
                  "student_at__name": ["icontains"],
                  "student_at__cod_aff_form": ["exact"]
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
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    filterset_class = UserProfileFilter
    filter_backends = (filters.DjangoFilterBackend,)
    permission_classes = [permissions.IsAuthenticated]
