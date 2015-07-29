from rest_framework import serializers

from .models import Comment

from django.db import IntegrityError
from django.core.exceptions import PermissionDenied


class CreateCommentSerializer(serializers.ModelSerializer):
    """
    Serializer Class to create Comment
    """
    author = serializers.SerializerMethodField()

    def get_author(self, obj):
        return obj.author.get_full_name()

    def create(self, validated_data):
        try:
            user = self.context['request'].user
            return Comment.objects.create(author=user, **validated_data)

        except IntegrityError, e:
            raise PermissionDenied

    class Meta():
        model = Comment
        fields = ('id', 'added_at', 'text', 'author' )
        read_only_fields = ('id', 'added_at', 'author', )


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
    author = serializers.SerializerMethodField()

    def get_author(self, obj):
        return obj.author.get_full_name()

    class Meta():
        model = Comment
        fields = ('id', 'text', 'author', 'added_at', )