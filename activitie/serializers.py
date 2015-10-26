from django.db import IntegrityError

from rest_framework import serializers


from .models import ActivitieParent, ActivitieChild


class ActivitieParentSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        try:
            user = self.context['request'].user
    
            activitie = ActivitieParent.objects.create(
                author=user,
                die_at=validated_data['die_at'],
                name=validated_data['name'],
                description=validated_data['description'])
            return activitie

        except IntegrityError, e:
            raise PermissionDenied


    class Meta():
        model = ActivitieParent
        fields = ('id', 'name', 'description', 'die_at')


class ActivitieChildSerializer(serializers.ModelSerializer):

    parent = serializers.CharField(required=True)
    status = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()

    def get_author(self, instance):
        return {'id': instance.author.id, 'name': instance.author.get_full_name()}

    def get_status(self, instance):
        return instance.STATUS[int(instance.status)]

    def create(self, validated_data):
        try:
            user = self.context['request'].user
            parent_activitie = validated_data['parent']
            parent_activitie = ActivitieParent.objects.get(pk=parent_activitie)

            try:
                previous = ActivitieChild.objects.get(author=user, parent=parent_activitie)
            except Exception, e:
                previous = []

            if previous:
                
                previous.file = validated_data['file']
                previous.save()
                return previous
            else:

                return ActivitieChild.objects.create(author=user, parent=parent_activitie, file=validated_data['file'])

        except IntegrityError, e:
            raise PermissionDenied

    def update(self, instance, validated_data):
        try:
            instance.file = validated_data.get('file', instance.file)
            instance.save()
            return instance
        except IntegrityError(e):
            raise PermissionDenied

    class Meta():
        model = ActivitieChild
        fields = ('id', 'parent', 'file', 'status', 'author', 'sent_at')
        read_only_fields = ('id', 'status', 'author', 'sent_at')