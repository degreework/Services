from django.db import IntegrityError


from rest_framework import serializers


from .models import ActivitieParent, ActivitieChild


class ActivitieParentSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        try:
            user = self.context['request'].user
            return ActivitieParent.objects.create(
                author=user,
                die_at=validated_data['die_at'],
                name=validated_data['name'],
                description=validated_data['description'])

        except IntegrityError, e:
            raise PermissionDenied  


    class Meta():
        model = ActivitieParent
        fields = ('id', 'name', 'description', 'die_at')


class ActivitieChildSerializer(serializers.ModelSerializer):

    parent = serializers.CharField(required=True)
    status = serializers.SerializerMethodField()


    def get_status(self, instance):
        return instance.STATUS[instance.status][1]

    def create(self, validated_data):
        try:

            user = self.context['request'].user
            parent_activitie = validated_data['parent']
            parent_activitie = ActivitieParent.objects.get(pk=parent_activitie)

            return ActivitieChild.objects.create(author=user, parent=parent_activitie, file=validated_data['file'])

        except IntegrityError, e:
            raise PermissionDenied

    class Meta():
        model = ActivitieChild
        fields = ('id', 'parent', 'file', 'status')
        read_only_fields = ('id', 'status')