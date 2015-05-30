
from rest_framework import serializers

from .models import User


class CreateUserSerializer(serializers.ModelSerializer):
    """
    Serializer Class to create users
    """
    class Meta():
        model = User
        fields = ('nick_name', 'first_name', 'last_name', 'email', 'codigo', 'plan', 'password')
        extra_kwargs = {'password': {'write_only': True}}


class UpdateUserSelializer(serializers.ModelSerializer):
    """
    Serializer class to update users
    """
    class Meta():
        model = User
        fields = ('nick_name', 'first_name', 'last_name', 'email', 'codigo', 'plan')


class ShortUserSerializer(serializers.ModelSerializer):
    """
    Serializer class to show info User "summary"
    """
    thumb = serializers.SerializerMethodField()

    class Meta():
        model = User
        fields = ('id', 'nick_name', 'thumb', 'first_name', 'last_name')

    def get_thumb(self, object):
        try:
            return object.photo['mini'].url
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
