# Third-party imports
from rest_framework import serializers, viewsets
from django_filters import rest_framework as filters
from rest_framework import permissions

# Local imports
from private_app.models import Link


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = [
            "link_type",
            "link_url",
        ]


class LinkFilter(filters.FilterSet):

    class Meta:
        # add possibility to filter by link type and link Url
        model = Link
        fields = {
            "link_type": ["icontains", "exact"],
            "link_url": ["icontains", "exact"],

        }


class LinkViewSet(viewsets.ModelViewSet):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
    filterset_class = LinkFilter
    filter_backends = [
        filters.DjangoFilterBackend,]
    permission_classes = [permissions.IsAuthenticated]
