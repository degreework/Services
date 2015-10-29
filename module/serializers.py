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


from badger.models import Badge
class ModuleUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer Class to create users
    """
    def update(self, instance, validated_data, **kwargs):
        print 'update module'
        try:

            instance.name = validated_data.get('name', instance.name)
            instance.description = validated_data.get('description', instance.description)
            instance.photo = validated_data.get('photo', instance.photo)
            
            badge = Badge.objects.get(slug=instance.slug)
            badge.title = instance.name
            badge.description = instance.description
            badge.save()
            
            instance.save()
            
            return instance
        except IntegrityError:
            raise PermissionDenied


    class Meta():
        model = Module
        fields = ('name', 'description', 'photo')
        read_only = ('id', 'slug',)