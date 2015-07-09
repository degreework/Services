from rest_framework import serializers

from .models import Comment

from django.db import IntegrityError
from django.core.exceptions import PermissionDenied


class CreateCommentSerializer(serializers.ModelSerializer):
    """
    Serializer Class to create Comment
    """
    def create(self, validated_data):
        try:
            author = self.context['request'].user.id
            #validated_data['author'] = author
            return Comment.objects.create(**validated_data)

        except IntegrityError, e:
            raise PermissionDenied

    class Meta():
        model = Comment
        fields = ('id', 'added_at', 'text', )
        read_only_fields = ('id', 'added_at', )


class UpdateCommentSelializer(serializers.ModelSerializer):
    """
    Serializer class to update Comment
    """
    class Meta():
        model = Comment
        fields = ('text', )


class ShortCommentSerializer(serializers.ModelSerializer):
    """
    Serializer class to show list of Comment
    """

    class Meta():
        model = Comment
        fields = ('id', 'text', 'added_at', )