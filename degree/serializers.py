from rest_framework import serializers

from .models import Degree


class DegreeSerializer(serializers.ModelSerializer):
    """
    Serializer Class to Degree
    """
    class Meta():
        model = Degree
        fields = ('code', 'name', )
