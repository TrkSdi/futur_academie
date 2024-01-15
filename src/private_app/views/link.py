# Third-party imports
from rest_framework import serializers

# Local imports
from private_app.models import Link


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = [
            "link_type",
            "link_url",
        ]
