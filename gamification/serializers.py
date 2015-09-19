from rest_framework import serializers

from badger import views
from badger.models import *
from badger.signals import *

from .models import Scores


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
