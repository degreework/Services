from django.http import Http404
from rest_framework import serializers

from .models import Ask, Answer

from django.db import IntegrityError
from django.core.exceptions import PermissionDenied


class CreateAskSerializer(serializers.ModelSerializer):
    """
    Serializer Class to create Asks
    """
    def create(self, validated_data):
        try:
            author = self.context['request'].user.id
            #validated_data['author'] = author
            return Ask.objects.create(**validated_data)

        except IntegrityError, e:
            raise PermissionDenied

    class Meta():
        model = Ask
        fields = ('title', 'text')


class UpdateAskSelializer(serializers.ModelSerializer):
    """
    Serializer class to update Asks
    """
    class Meta():
        model = Ask
        fields = ('title', 'html', 'text', 'summary')


class ShortAskSerializer(serializers.ModelSerializer):
    """
    Serializer class to show list of Asks
    """

    class Meta():
        model = Ask
        fields = ('id', 'title', 'added_at')

class AskDetailSerializer(serializers.ModelSerializer):
    """
    Serializer class to show detailed Ask
    """

    class Meta():
        model = Ask
        fields = ('id', 'title', 'text', 'added_at')


"""Classes for Answers"""

class AnswerCreateSerializer(serializers.ModelSerializer):
    """
    Serializer Class to create Answer
    """
    ask = serializers.CharField(required=True)


    def validate_ask(self, value):
        try:
            ask = Ask.objects.get(pk=value)
        except Ask.DoesNotExist:
            raise Http404("La pregunta no existe")
        return ask

    def create(self, validated_data):
        try:
            author = self.context['request'].user.id
            #print validated_data['ask']
            #validated_data['author'] = author
            #validated_data['ask'] = Ask.objects.get(pk=validated_data['parent'])
            return Answer.objects.create(**validated_data)

        except IntegrityError, e:
            print e
            raise PermissionDenied

    class Meta():
        model = Answer
        fields = ('id', 'ask', 'text', 'added_at')
        read_only_fields = ('id', 'added_at', )

class AnswerUpdateSelializer(serializers.ModelSerializer):
    """
    Serializer class to update Answer
    """
    class Meta():
        model = Answer
        fields = ('html', 'text', 'summary')


class AnswerShortSerializer(serializers.ModelSerializer):
    """
    Serializer class to show list of Answer
    """

    class Meta():
        model = Answer
        fields = ('id', 'text', 'added_at')

