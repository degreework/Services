from rest_framework import serializers

from .models import Module


class ModuleSerializer(serializers.ModelSerializer):
    """
    Serializer Class to create users
    """
    class Meta():
        model = Module
        fields = ('name', 'description', 'slug', 'id')
        read_only = ('id', 'slug',)
