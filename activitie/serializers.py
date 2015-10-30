from django.db import IntegrityError

from rest_framework import serializers


from .models import ActivitieParent, ActivitieChild


class ActivitieParentSerializer(serializers.ModelSerializer):
    child = serializers.SerializerMethodField()

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

    def get_child(self, obj):
        try:
            return ActivitieChildSerializer(ActivitieChild.objects.get(parent=obj, author=self.context['request'].user)).data
        except ActivitieChild.DoesNotExist:
            return ''


    class Meta():
        model = ActivitieParent
        fields = ('id', 'name', 'description', 'die_at', 'child')



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

                activitie = ActivitieChild.objects.create(author=user, parent=parent_activitie, file=validated_data['file'])
                
                #create Stream at User's wall
                from actstream import action
                action.send(user, verb='enviado', action_object=activitie, target=parent_activitie)

                return activitie

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