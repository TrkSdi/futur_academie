# Third-party imports
from rest_framework import serializers, viewsets

# Local imports
from private_app.models import Link


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = [
            "link_type",
            "link_url",
        ]


class LinkViewSet(viewsets.ModelViewSet):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
