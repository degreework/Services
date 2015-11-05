from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import get_object_or_404


from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from project.permissions import IsTeacher

from .serializers import MaterialFileSerializer, MaterialLinkSerializer, MaterialSerializer

class MaterialFileCreateView(viewsets.ModelViewSet):
    """
    API endpoint for creating Material
    """
    serializer_class = MaterialFileSerializer
    permission_classes = (IsTeacher, )


class MaterialLinkCreateView(viewsets.ModelViewSet):
    """
    API endpoint for creating Material
    """
    serializer_class = MaterialLinkSerializer
    permission_classes = (IsTeacher, )


from .models import Material, MaterialLink, MaterialFile
class MaterialListView(generics.ListAPIView):
    """
    View to list all Material
    """
    #add permission
    permission_classes = (IsAuthenticated, )
    serializer_class = MaterialSerializer
    paginate_by = 5

    def get_queryset(self):
        return Material.objects.select_subclasses("materialfile", "materiallink")


class MaterialReadView(viewsets.ModelViewSet):
    """
    API endpoint for retreive a Material
    """
    serializer_class = MaterialSerializer
    permission_classes = (IsAuthenticated, )

    def retrieve(self, request, pk=None):
        serializer = MaterialSerializer( Material.objects.filter(pk=pk).select_subclasses()[0] )
        return Response(serializer.data)