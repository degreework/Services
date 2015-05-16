

from .serializers import CreateUserSerializer, UpdateUserSelializer, ShortUserSerializer
from rest_framework.permissions import AllowAny

from rest_framework import viewsets

class CreateUserView(viewsets.ModelViewSet):
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
    permission_classes = (IsSelf, )


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