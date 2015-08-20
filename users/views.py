# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate
from django.core.urlresolvers import reverse
from django.http import Http404

from rest_framework import viewsets, generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope, TokenHasScope

from .models import User
from .permissions import IsSelf
from .serializers import CreateUserSerializer, UpdateUserSelializer, ShortUserSerializer, UpdatePasswordUserSelializer, RecoveryPasswordSelializer


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



## NO WORKS
from django.core.mail import send_mail

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
        return Response(csrf(request))
    

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
        response = password_reset(
            request,
            template_name='reset.html',
            extra_context = request.POST,
            email_template_name='reset_email.html',
            subject_template_name='reset_subject.txt',
            post_reset_redirect=reverse('recovery-password'))
        print response
        print response.status_code

        if 302 == response.status_code:
            email = request.POST.get('email', False)
            print response
            return Response({'email':email}, status=status.HTTP_200_OK)

        return Response({}, status=status.HTTP_400_BAD_REQUEST)


from django.views.decorators.debug import sensitive_post_parameters


class RecoveryPassword_confirm(APIView):
    """
    API endpoint for recovery a User password
    """
    serializer_class = UpdatePasswordUserSelializer
    permission_classes = (AllowAny, )
    
    def post(self, request, uidb64=None, token=None):
        print request.POST
        print uidb64
        print token
        response = password_reset_confirm(
            request,
            template_name='reset.html',
            uidb64=uidb64,
            token=token,
            post_reset_redirect=reverse('password_reset_done'))

        print response
        
        return Response({}, status=status.HTTP_200_OK)


class RecoveryPasswordDone(APIView):
    """
    API endpoint for recovery a User password
    """
    permission_classes = (AllowAny, )
    
    def get(request, *args, **kwargs):
        return Response({'msg': 'Password changed'}, status=status.HTTP_200_OK)

from rest_framework.decorators import api_view
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
class PermissionsCurrentUser(APIView):
    """
    Retrieve permissions list
    """
    #permission_classes = (IsAuthenticated, )
    permission_classes = (AllowAny, )

    def get(self, request, token):
        current_token = AccessToken.objects.get(token=token)
        return Response(current_token.scope)