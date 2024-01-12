# Third-party imports
from rest_framework import serializers, viewsets

# Local imports
from private_app.models import UserProfile, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        user_extended = UserSerializer(source='users', read_only=False)
        read_only_fields = ("id",)
        fields = ["id", "user_extended", "user", "image_profile",
                  "url_tiktok", "url_instagram", "about_me", "is_public", "student_at"]


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
