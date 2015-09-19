from django.http import Http404
from django.db import IntegrityError
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied
from django.conf import settings

from rest_framework import serializers

from reminder.signals import forum_answered, forum_ask_updated

from .models import Ask, Answer


class CreateAskSerializer(serializers.ModelSerializer):
    """
    Serializer Class to create Asks
    """
    def create(self, validated_data):
        try:
            user = self.context['request'].user
            return Ask.objects.create(author=user, **validated_data)
        except IntegrityError(e):
            raise PermissionDenied

    class Meta():
        model = Ask
        fields = ('title', 'text', 'id')
        read_only_fields = ('id', )


class UpdateAskSelializer(serializers.ModelSerializer):
    """
    Serializer class to update Asks
    """
    def update(self, instance, validated_data):
        print "update"
        try:
            instance.title = validated_data.get('title', instance.title)
            instance.text = validated_data.get('text', instance.text)
            instance.save()

            if getattr(settings, 'NOTIFICATIONS', False):
                forum_ask_updated.send(sender=UpdateAskSelializer, ask=instance)

            return instance
        except IntegrityError(e):
            raise PermissionDenied

    class Meta():
        model = Ask
        fields = ( 'title', 'text')
        #read_only_fields = ('id')


class ShortAskSerializer(serializers.ModelSerializer):
    """
    Serializer class to show list of Asks
    """
    count = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()

    def get_author(self, obj):
        return {'id': obj.author.id, 'name': obj.author.get_full_name()}

    def get_count(self,obj):
        return Answer.objects.filter(ask=obj).count()

    class Meta():
        model = Ask
        fields = ('id', 'title', 'added_at', 'author', 'count')


class AskDetailSerializer(serializers.ModelSerializer):
    """
    Serializer class to show detailed Ask
    """
    author = serializers.SerializerMethodField()

    def get_author(self, obj):
        return {'id': obj.author.id, 'name': obj.author.get_full_name()}

    class Meta():
        model = Ask
        fields = ( 'title', 'text', 'added_at', 'author', 'id')


"""Classes for Answers"""

class AnswerCreateSerializer(serializers.ModelSerializer):
    """
    Serializer Class to create Answer
    """
    ask = serializers.CharField(required=True)
    author = serializers.SerializerMethodField()

    def get_author(self, obj):
        return {'id':obj.author.id, 'name':obj.author.get_full_name()}

    def validate_ask(self, value):
        try:
            ask = Ask.objects.get(pk=value)
        except Ask.DoesNotExist:
            raise Http404("La pregunta no existe")
        return ask

    def create(self, validated_data):
        try:
            user = self.context['request'].user
            answer = Answer.objects.create(author=user, **validated_data)
            
            if getattr(settings, 'NOTIFICATIONS', False):
                forum_answered.send(sender=AnswerCreateSerializer, ask=answer.ask, answer=answer, author=user)
            
            return answer

        except IntegrityError,e:
            raise PermissionDenied

    class Meta():
        model = Answer
        fields = ( 'id', 'ask', 'text', 'author', 'added_at')
        read_only_fields = ( 'id', 'added_at', 'author', )


class AnswerUpdateSelializer(serializers.ModelSerializer):
    """
    Serializer class to update Answer
    """
    ask = serializers.CharField(required=True)
    author = serializers.SerializerMethodField()

    def get_author(self, obj):
        return obj.author.get_full_name()

    def validate_ask(self, value):
        try:
            ask = Ask.objects.get(pk=value)
        except Ask.DoesNotExist:
            raise Http404("La pregunta no existe")
        return ask

    def create(self, validated_data):
        try:
            user = self.context['request'].user
            return Answer.objects.create(author=user, **validated_data)

        except IntegrityError(e):
            raise PermissionDenied


    class Meta():
        model = Answer
        fields = ('id', 'ask', 'text', 'author', 'added_at')
        read_only_fields = ('id', 'added_at', 'author', )


class AnswerShortSerializer(serializers.ModelSerializer):
    """
    Serializer class to show list of Answer
    """
    author = serializers.SerializerMethodField()

    def get_author(self, obj):
        return {'id': obj.author.id, 'name': obj.author.get_full_name()}

    class Meta():
        model = Answer
        fields = ('id', 'text', 'added_at', 'author', 'ask')

