from rest_framework import serializers

from badger import views
from badger.models import *
from badger.signals import *

from .models import Scores, Votes


class BadgeCreateSerializer(serializers.ModelSerializer):
    """
    Serializer Class Badge
    """

    class Meta():
        model = Badge


class AwardCreateSerializer(serializers.ModelSerializer):
    """
    Serializer Class Award
    """

    class Meta():
        model = Award


class ProgressCreateSerializer(serializers.ModelSerializer):
    """
    Serializer Class Progress
    """

    class Meta():
        model = Progress


#----------------

class ScoresUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer Class Nomination
    """

    class Meta():
        model = Scores


# -------
# Votes
#

from django.db import IntegrityError
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist


class VotesSerializer(serializers.ModelSerializer):
    """
    Serializer Class to Votes
    """
    previous = serializers.SerializerMethodField()

    def get_previous(self, obj_thread):
        return self.previous

    def create(self, validated_data):
        try:
            user = self.context['request'].user
            thread = validated_data['thread']
            vote = validated_data['vote']
            try:
                self.previous = int(Votes.objects.get(thread=thread, author=user).vote)
            except ObjectDoesNotExist, e:
                self.previous = ""

            voted = Votes.create(author=user, thread=thread, vote=vote)
            return voted

        except IntegrityError, e:
            raise PermissionDenied

    class Meta():
        model = Votes
        fields = ('thread', 'vote', 'previous',  )
        read_only_fields = ('previous', )


class ListVotesSerializer(serializers.ModelSerializer):
    thread = serializers.SerializerMethodField()
    up_votes = serializers.SerializerMethodField()
    down_votes = serializers.SerializerMethodField()
    
    def get_thread(self, obj_thread):
        return obj_thread.pk
    
    def get_up_votes(self, obj_thread):
        # 0 is up vote
        return Votes.objects.filter(thread=obj_thread.pk, vote=0).count()

    def get_down_votes(self, obj_thread):
        # 1 is down vote
        return Votes.objects.filter(thread=obj_thread.pk, vote=1).count()

    class Meta():
        model = Votes
        fields = ('thread', 'up_votes', 'down_votes', )

