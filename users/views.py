# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate
from django.core.urlresolvers import reverse
from django.http import Http404
from django import middleware

from rest_framework import viewsets, generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope, TokenHasScope

from .models import User
from .permissions import IsSelf
from .serializers import (
        CreateUserSerializer,
        UpdateUserSelializer,
        ShortUserSerializer,
        UpdatePasswordUserSelializer,
        RecoveryPasswordSelializer,
        RecoveryPasswordConfirmSelializer)


class UserCreateView(viewsets.ModelViewSet):
    """
    API endpoint for creating a User
    """
    serializer_class = CreateUserSerializer
    permission_classes = (AllowAny, )


class UserUpdate(viewsets.ModelViewSet):
    """
    API endpoint for retrieve, update, destroy a User
    """
    queryset = User.objects.all()
    serializer_class = UpdateUserSelializer
    permission_classes = (IsSelf, )


class UserDetail(APIView):
    """
    Retrieve a User
    """
    permission_classes = (IsAuthenticated, )

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = ShortUserSerializer(user)
        return Response(serializer.data)


#from rest_framework import authentication
class UserList(generics.ListAPIView):
    """
    View to list all aks in the foro.
    """
    #authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (IsAuthenticated, )
    queryset = User.objects.all()
    serializer_class = ShortUserSerializer
    paginate_by = 10


class UserCurrent(APIView):
    """
    Retrieve current logged user
    """
    permission_classes = (IsAuthenticated, IsSelf, )

    def get(self, request):
        serializer = ShortUserSerializer(request.user)
        return Response(serializer.data)


class UserPassword(APIView):
    """
    API endpoint for change User password
    """
    serializer_class = UpdatePasswordUserSelializer
    permission_classes = (IsAuthenticated, IsSelf, )
    

    def post(self, request, *args, **kwargs):
        response_status = status.HTTP_401_UNAUTHORIZED
        response_data = ""
        
        if request.POST.get('new', False) == request.POST.get('old', False):
            response_data = "No se hizo nada"
        else:
            email = request.user.email
            user = authenticate(username=email, password=request.POST['old'])
            if user is not None and user.is_active:
                user.set_password(request.POST['new'])
                user.save()
                response_data = "Cambiado"
                response_status = status.HTTP_200_OK
            else:
                response_data = "Contraseña incorrecta"
        print response_data
        return Response(response_data, status=response_status)


from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'create': reverse('user_create', request=request, format=format),
        
        # due to DRF Issue #3190, this (parametrized url to api root) can't be enabled
        #'update': reverse('user-update', request=request, format=format),
        
        'current': reverse('user-current', request=request, format=format),
    })


from oauth2_provider.models import AccessToken
from django.contrib.auth.models import Permission
class PermissionsCurrentUser(APIView):
    """
    Retrieve permissions list
    """
    #permission_classes = (IsAuthenticated, )
    permission_classes = (AllowAny, )

    def get(self, request, token):
        current_token = AccessToken.objects.get(token=token)
        #print(current_token.scope)

        permissions = current_token.user.get_all_permissions()
        #print("user", current_token.user)
        #print("permissions", permissions)
        scope = " "
        for p in permissions:
            scope += p + " "

        #print(scope)
        return Response(scope)


# Import the built-in password reset view and password reset confirmation view.
from django.contrib.auth.views import password_reset, password_reset_confirm
from django.template.context_processors import csrf

class RecoveryPassword(APIView):
    """
    API endpoint for crecovery a User password
    """
    serializer_class = RecoveryPasswordSelializer
    permission_classes = (AllowAny, )

    def get(self, request, *args, **kwargs):
        print("GET")
        c = middleware.csrf.get_token(request)
        print(c)
        return Response({'csrf_token':c})
    

    def post(self, request, *args, **kwargs):
        print request.POST
        """
        send_mail(
            'Important Advice',
            'You has been hacked by an anonymous user at facebook.com, please go into facebook.com and changes right now your current password',
            'app@gmail.com',
            ['miguel.angel.bernal@correounivalle.edu.co'],
            fail_silently=False
            )
        """
        response = password_reset(request)
        return response
        

@api_view(('GET',))
@permission_classes((AllowAny, ))
def password_reset_done(request):
    return Response(
        {
        'msg':
        """Le hemos enviado por email las instrucciones para restablecer la contraseña, si es que existe una cuenta con la dirección electrónica que indicó. Debería recibirlas en breve.
Si no recibe un correo, por favor asegúrese que ha introducido la dirección de correo con la que se registró y verifique su carpeta de spam."""
        }
    )

@api_view(('GET',))
@permission_classes((AllowAny, ))
def password_reset_complete(request):
    return Response(
        {
        'msg': "Su contraseña ha sido establecida. Ahora puede seguir adelante e iniciar sesión."
        }
    )

from django.views.decorators.debug import sensitive_post_parameters

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

from rest_framework.serializers import ValidationError
from django.contrib.auth import get_user_model
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator


class RecoveryPassword_confirm(APIView):
    """
    API endpoint for recovery a User password
    """
    serializer_class = RecoveryPasswordConfirmSelializer
    permission_classes = (AllowAny, )

    def get(self, request, *args, **kwargs):
        print("GET")
        c = middleware.csrf.get_token(request)
        print(c)
        return Response(c)
    
    #@method_decorator(sensitive_post_parameters())
    #@csrf_protect
    #@method_decorator(csrf_protect)
    #@sensitive_post_parameters()
    def post(self, request, uidb64=None, token=None):
        print request.POST
        print uidb64
        print token
        if request.POST.get('new_password1') != request.POST.get('new_password2'):
            raise ValidationError("Passwords don't match")


        """
        View that checks the hash in a password reset link and presents a
        form for entering a new password.
        """
        UserModel = get_user_model()
        assert uidb64 is not None and token is not None  # checked by URLconf
        try:
            # urlsafe_base64_decode() decodes to bytestring on Python 3
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = UserModel._default_manager.get(pk=uid)
        except (UserModel.DoesNotExist):
            user = None


        # si el link aún es válido
        if user is not None and default_token_generator.check_token(user, token):
            response = password_reset_confirm(
                request,
                uidb64=uidb64,
                token=token)
            return response
        else:
            return Response({'msg': "El enlace de restablecimiento de contraseña era invalido, seguramente por haberse utilizado previamente. Por favor, solicite un nuevo restablecimiento de contraseña."})
        