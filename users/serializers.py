from rest_framework import serializers

from .models import User

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
            #from gamification.signals import set_progress_user
            #set_progress_user.send(sender=CreateUserSerializer, user= user)
            
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
            #from gamification.signals import set_progress_user
            #set_progress_user.send(sender=CreateUserSerializer, user= user)

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


from actstream.models import Action

class StreamSerializer(serializers.Serializer):
    """
    Serializer class to render User's Wall
    """
    timestamp = serializers.SerializerMethodField()
    verb = serializers.SerializerMethodField()
    object = serializers.SerializerMethodField()
    target = serializers.SerializerMethodField()
    module = serializers.SerializerMethodField()

    def get_timestamp(self, object):
        return object.timestamp

    def get_verb(self, object):
        return object.verb

    def get_object(self, object):
        try:
            action_object = {
                'id': object.action_object.pk,
                'type': object.action_object.css_class(),
                'detail': object.action_object.detail()
            }

        except AttributeError, e:
            print e
            action_object = {}

        return action_object 

    def get_target(self, object):
        try:
            target = {
            'id': object.target.pk,
            'type': object.target.css_class(),
            'detail': object.target.detail()
            }
        except AttributeError:
            return ''
        return target

    def get_module(self, object):

        from django.contrib.contenttypes.models import ContentType
        from forum.models import Ask, Answer
        from wiki.models import pageComments
        from module.models import Forum_wrap, Wiki_wrap, Activitie_wrap, Module
        from comment.models import Comment
        from activitie.models import ActivitieParent, ActivitieChild
        module = {}


        """
        if object.action_object_content_type == ContentType.objects.get_for_model(Module):
            module = {
                'name' : object.action_object.name,
                'slug' : object.action_object.slug 
            }
        """

        if object.action_object_content_type == ContentType.objects.get_for_model(Ask):
            wrap =  Forum_wrap.objects.get(ask=object.action_object)
            module = {
                'name' : wrap.module.name,
                'slug' : wrap.module.slug 
            }
        elif object.action_object_content_type == ContentType.objects.get_for_model(Answer):
            wrap =  Forum_wrap.objects.get(ask=object.target)
            module = {
                'name' : wrap.module.name,
                'slug' : wrap.module.slug 
            }

        elif object.action_object_content_type == ContentType.objects.get_for_model(ActivitieChild):
            wrap =  Activitie_wrap.objects.get(activitie=object.target)
            module = {
                'name' : wrap.module.name,
                'slug' : wrap.module.slug 
            }

        elif object.target_content_type == ContentType.objects.get_for_model(Module):
                module = {
                    'name' : object.target.name,
                    'slug' : object.target.slug 
                }

        elif object.action_object_content_type == ContentType.objects.get_for_model(Comment):
            
            if object.target_content_type == ContentType.objects.get_for_model(Ask):
                wrap =  Forum_wrap.objects.get(ask=object.target)
                module = {
                    'name' : wrap.module.name,
                    'slug' : wrap.module.slug 
                }
            elif object.target_content_type == ContentType.objects.get_for_model(Answer):
                wrap =  Forum_wrap.objects.get(ask=object.target.ask)
                module = {
                    'name' : wrap.module.name,
                    'slug' : wrap.module.slug 
                }    
            
            elif object.target_content_type == ContentType.objects.get_for_model(pageComments):
                wrap =  Wiki_wrap.objects.get(page=object.target.page)
                module = {
                    'name' : wrap.module.name,
                    'slug' : wrap.module.slug 
                }
                


        return module

    class Meta():
        model = Action
        fields = ('timestamp', 'verb', 'object', 'target', 'module')
