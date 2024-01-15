# Third-party imports
from django_filters import rest_framework as filters
from rest_framework import serializers, viewsets
from rest_framework import permissions

# Local imports
from private_app.models import Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ["street_address", "postcode", "locality", "geolocation"]


class AddressFilter(filters.FilterSet):
    class Meta:
        model = Address
        fields = {
            "street_address": ["icontains"],
            "postcode": ["contains", "exact"],
            "locality": ["icontains", "exact"],
        }


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    filterset_class = AddressFilter
    filter_backends = (filters.DjangoFilterBackend,)
    permission_classes = [permissions.IsAuthenticated]
