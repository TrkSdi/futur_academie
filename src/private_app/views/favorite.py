# Third-party imports
from rest_framework import serializers, viewsets

# Local imports
from private_app.models import Favorite


class FavoriteSeralizer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ["id","user", "study_program", "note", "status"]


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSeralizer