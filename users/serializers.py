from rest_framework import serializers

from .models import User

class CreateUserSerializer(serializers.ModelSerializer):
    """
    Serializer Class to create users
    """

    def save(self):
        user = User.objects.create_user(
            self.validated_data['email'],
            self.validated_data['codigo'],
            self.validated_data['first_name'],
            self.validated_data['last_name'],
            self.validated_data['password'],
            #self.validated_data.get('plan', None)
            )
        return user

    class Meta():
        model = User
        fields = ('first_name', 'last_name', 'email', 'codigo', 'password')
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
        fields = ('id', 'thumb', 'first_name', 'last_name', 'email', 'codigo', 'plan')

    def get_thumb(self, object):
        try:
            return [object.photo['mini'].url, object.photo['user_profile'].url]
        except:
            #poner algo menos feo XD
            return ""


class UpdatePasswordUserSelializer(serializers.Serializer):
    """
    Serializer class to update password User
    """
    new = serializers.CharField(style={'input_type': 'password'})
    old = serializers.CharField(style={'input_type': 'password'})
    
    class Meta():
        model = User
        fields = ('new', 'old', )


class RecoveryPasswordSelializer(serializers.Serializer):
    """
    Serializer class to recovery password User
    """
    email = serializers.EmailField()
