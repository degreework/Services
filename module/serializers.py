from rest_framework import serializers
from django.db import IntegrityError
from django.core.exceptions import PermissionDenied
from .models import Module

from django.conf import settings
from reminder.signals import create_module


class ModuleSerializer(serializers.ModelSerializer):
    """
    Serializer Class to create users
    """
    photo = serializers.SerializerMethodField()

    def create(self, validated_data):
        try:        
            module = Module.objects.create(**validated_data)

            if getattr(settings, 'NOTIFICATIONS', False):
                create_module.send(sender=ModuleSerializer, author=self.context['request'].user, module=module)

            return module
        except IntegrityError, e:
            raise PermissionDenied

    def get_photo(self, obj):
        return obj.photo.url


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
