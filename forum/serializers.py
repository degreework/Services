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
            validated_data['author'] = author
            return Ask.objects.create(**validated_data)

        except IntegrityError, e:
            raise PermissionDenied

    class Meta():
        model = Ask
        fields = ('title', 'html', 'text', 'summary')


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
        fields = ('id', 'title', 'summary')



"""Classes for Answers"""


class AnswerCreateSerializer(serializers.ModelSerializer):
    """
    Serializer Class to create Answer
    """
    def create(self, validated_data):
        try:
            author = self.context['request'].user.id
            validated_data['author'] = author
            return Answer.objects.create(**validated_data)

        except IntegrityError, e:
            raise PermissionDenied

    class Meta():
        model = Answer
        fields = ('html', 'text')

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
        fields = ('id', 'summary', 'added_at')

