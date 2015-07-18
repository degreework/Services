# -*- coding: utf-8 -*-

from django.contrib.auth import authenticate

from rest_framework import viewsets, generics, status
from .serializers import CreateUserSerializer, UpdateUserSelializer, ShortUserSerializer, GroupSerializer, UpdatePasswordUserSelializer
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework import viewsets


from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope, TokenHasScope

class UserCreateView(viewsets.ModelViewSet):
    """
    API endpoint for creating a User
    """
    serializer_class = CreateUserSerializer
    permission_classes = (AllowAny, )


from .models import User
from .permissions import IsSelf

class UserUpdate(viewsets.ModelViewSet):
    """
    API endpoint for retrieve, update, destroy a User
    """
    queryset = User.objects.all()
    serializer_class = UpdateUserSelializer
    permission_classes = (TokenHasReadWriteScope, IsSelf, )

from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404


class UserDetail(APIView):
    """
    Retrieve a User
    """
    permission_classes = (AllowAny, )

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = ShortUserSerializer(user)
        return Response(serializer.data)


from rest_framework.views import APIView
from rest_framework import authentication

class UserList(generics.ListAPIView):
    """
    View to list all aks in the foro.
    """

    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = ShortUserSerializer
    paginate_by = 10


from django.contrib.auth.models import Group
from oauth2_provider.ext.rest_framework import OAuth2Authentication

class GroupViewSet(viewsets.ModelViewSet):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasReadWriteScope]
    permission_classes = [IsAuthenticated, TokenHasScope]
    required_scopes = ['groups']
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class UserCurrent(APIView):
    """
    Retrieve current logged user
    """
    permission_classes = (TokenHasReadWriteScope, IsSelf, )

    def get(self, request):
        user = request.user
        serializer = ShortUserSerializer(user)
        return Response(serializer.data)


class UserPassword(generics.UpdateAPIView):
    """
    API endpoint for change User password
    """
    serializer_class = UpdatePasswordUserSelializer
    permission_classes = (TokenHasReadWriteScope, IsSelf, )
    

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
