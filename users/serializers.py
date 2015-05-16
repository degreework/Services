
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
        fields = ('nick_name', 'first_name', 'last_name', 'email', 'codigo', 'plan', 'is_active')
        read_only_fields = ('codigo', 'plan')


class ShortUserSerializer(serializers.ModelSerializer):
    """
    Serializer class to show info User "summary"
    """
    class Meta():
        model = User
        fields = ('id', 'nick_name', 'first_name', 'last_name')
