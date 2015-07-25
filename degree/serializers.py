from rest_framework.serializers import ModelSerializer

from .models import Degree

class DegreeSerializer(ModelSerializer):
    """
    Serializer Class to Degree
    """
    class Meta():
        model = Degree
        fields = ('code', 'name', )
