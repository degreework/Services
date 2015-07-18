
from rest_framework import serializers

from .models import User


class CreateUserSerializer(serializers.ModelSerializer):
    """
    Serializer Class to create users
    """

    def get_plan(self):
        print self
        return '0'

    class Meta():
        model = User
        fields = ('first_name', 'last_name', 'email', 'codigo', 'plan', 'password')
        extra_kwargs = {'password': {'write_only': True}}


class UpdateUserSelializer(serializers.ModelSerializer):
    """
    Serializer class to update users
    """
    class Meta():
        model = User
        fields = ('first_name', 'last_name', 'email', 'codigo', 'plan', 'photo')

    

class ShortUserSerializer(serializers.ModelSerializer):
    """
    Serializer class to show info User "summary"
    """
    thumb = serializers.SerializerMethodField()

    class Meta():
        model = User
        fields = ('id', 'thumb', 'first_name', 'last_name')

    def get_thumb(self, object):
        try:
            photos = [object.photo['mini'].url, object.photo['user_profile'].url]
            return photos
        except:
            #poner algo menos feo XD
            return "No found"

class UpdatePasswordUserSelializer(serializers.ModelSerializer):
    """
    Serializer class to update password User
    """
    class Meta():
        model = User
        fields = ('password', )

from django.contrib.auth.models import Group

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
