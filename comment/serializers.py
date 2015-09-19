from django.db import IntegrityError
from django.core.exceptions import PermissionDenied
from django.conf import settings

from rest_framework import serializers

from reminder.signals import post_comment

from .models import Comment



class CreateCommentSerializer(serializers.ModelSerializer):
    """
    Serializer Class to create Comment
    """
    author = serializers.SerializerMethodField()
    parent = serializers.CharField()
    
    def get_author(self, obj):
        return {'id': obj.author.id, 'name': obj.author.get_full_name()}

    def create(self, validated_data):
        try:
            user = self.context['request'].user
            thread = validated_data['parent']
            from post_framework.models import Thread
            thread = Thread.objects.get(pk=thread)

            comment = Comment.objects.create(author=user, parent=thread, text=validated_data['text'])
            
            if getattr(settings, 'NOTIFICATIONS', False):
                post_comment.send(sender=CreateCommentSerializer, post=thread, comment=comment, author=user)
            
            return comment

        except IntegrityError, e:
            raise PermissionDenied

    class Meta():
        model = Comment
        fields = ('id', 'added_at', 'author', 'text', 'parent', )
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
        return {'id': obj.author.id, 'name': obj.author.get_full_name()}

    class Meta():
        model = Comment
        fields = ('id', 'text', 'author', 'added_at', )