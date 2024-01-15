# Third-party imports
from django_filters import rest_framework as filters
from rest_framework import serializers, viewsets
from rest_framework import permissions

# Local imports
from private_app.models import Address


class AddressSerializerPublic(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ["street_address", "postcode", "locality", "geolocation"]
        read_only_fields = ["street_address", "postcode", "locality", "geolocation"]


class AddressFilterPublic(filters.FilterSet):
    class Meta:
        model = Address
        fields = {
            "street_address": ["icontains"],
            "postcode": ["contains", "exact"],
            "locality": ["icontains", "exact"],
        }


class AddressViewSetPublic(viewsets.ReadOnlyModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializerPublic
    filterset_class = AddressFilterPublic
    filter_backends = (filters.DjangoFilterBackend,)
    permission_classes = [permissions.AllowAny]
