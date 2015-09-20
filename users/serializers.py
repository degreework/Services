from rest_framework import serializers

from .models import User
from badger.models import Badge, Progress
from badger.utils import get_badge
from gamification.serializers import ProgressCreateSerializer

class CreateUserSerializer(serializers.ModelSerializer):
    """
    Serializer Class to create users
    """
    
    def save(self):
        if self.validated_data['plan'] == None:
            user = User.objects.create_user(
                self.validated_data['email'],
                self.validated_data['codigo'],
                self.validated_data['first_name'],
                self.validated_data['last_name'],
                self.validated_data['password'],
                #self.validated_data['plan']
                #self.validated_data.get('plan', None)
                )
            # crea el progreso de la insignia con la cual inicia el usuario
            #badge = get_badge('slug')
            #progress = badge.progress_for(user)
            #progress.save()
            
            return user
        else:
            user = User.objects.create_user(
                self.validated_data['email'],
                self.validated_data['codigo'],
                self.validated_data['first_name'],
                self.validated_data['last_name'],
                self.validated_data['password'],
                self.validated_data['plan']
                )
            
            # crea el progreso de la insignia con la cual inicia el usuario
            badge = get_badge('slug')
            progress = badge.progress_for(user)
            progress.save()
            return user

    
    """
    def create(self, validated_data):
        return User.objects.create(**validated_data)
    """
    class Meta():
        model = User
        fields = ('first_name', 'last_name', 'email', 'codigo', 'plan', 'password', 'id')
        read_only = ('id')
        extra_kwargs = {'password': {'write_only': True}, 'id':{'read_only':True}}


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


class RecoveryPasswordConfirmSelializer(serializers.Serializer):
    """
    Serializer class to recovery password User
    """
    new_password1 = serializers.CharField(style={'input_type': 'password'})
    new_password2 = serializers.CharField(style={'input_type': 'password'})
