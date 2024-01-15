# Third-party imports
from rest_framework import serializers, viewsets

# Local imports
from private_app.models import UserProfile, User
from .favorite import FavoriteSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]


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
