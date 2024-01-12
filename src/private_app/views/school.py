# Third-party imports
from rest_framework import serializers, viewsets

# Local imports
from private_app.models import School
    
    
class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ['UAI_code','name', 'school_url', 'description', 'address', 'school_type']
        

class SchoolViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer