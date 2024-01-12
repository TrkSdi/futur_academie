# Third-party imports
from rest_framework import serializers, viewsets

# Local imports
from private_app.models import Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ["street_address", "postcode", "locality", "geolocation"]


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
