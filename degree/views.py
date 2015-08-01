from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import Degree
from .serializers import DegreeSerializer

class DegreeList(generics.ListAPIView):
    """
    View to list all Degree
    """
    permission_classes = (AllowAny, )
    queryset = Degree.objects.all()
    serializer_class = DegreeSerializer