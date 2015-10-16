from rest_framework import serializers
from django.db import IntegrityError
from .models import Module
from  gamification.signals import createBadgeModule


class ModuleSerializer(serializers.ModelSerializer):
    """
    Serializer Class to create users
    """
    def create(self, validated_data):
    	try:		
    		module = Module.objects.create(**validated_data)
    		createBadgeModule.send(sender=ModuleSerializer, module=module)
    		return module
    	except IntegrityError, e:
            raise PermissionDenied



    class Meta():
        model = Module
        fields = ('name', 'description', 'slug', 'photo', 'id')
        read_only = ('id', 'slug',)
