from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404


from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import ActivitieParent, ActivitieChild
from .serializers import ActivitieParentSerializer, ActivitieChildSerializer

from .permissions import IsAuthor

class ActivitieParentCreateView(viewsets.ModelViewSet):
    """
    API endpoint for creating an Activitie
    """
    serializer_class = ActivitieParentSerializer
    permission_classes = (IsAuthenticated, IsAuthor, )


class ActivitieParentUpdateView(viewsets.ModelViewSet):
    """
    API endpoint for updating an Activitie
    """
    queryset = ActivitieParent.objects.all()
    serializer_class = ActivitieParentSerializer
    permission_classes = (IsAuthenticated, IsAuthor, )

    """
    def get_queryset(self):
        print self.kwargs['pk']
        try:
            queryset = ActivitieParent.objects.get(id=self.kwargs['pk'])

        except ObjectDoesNotExist:
            raise Http404()
        
        return queryset
    """

class ActivitieParentListView(generics.ListAPIView):
    """
    View to list all Activities
    """
    queryset = ActivitieParent.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = ActivitieParentSerializer
    paginate_by = 5

    



class ActivitieChildCreateView(viewsets.ModelViewSet):
    """
    API endpoint for creating an Activitie
    """
    serializer_class = ActivitieChildSerializer
    permission_classes = (IsAuthenticated, )


class ActivitieChildUpdateCreateView(viewsets.ModelViewSet):
    """
    API endpoint for updating an Activitie
    """
    queryset = ActivitieChild.objects.all()
    serializer_class = ActivitieChildSerializer
    permission_classes = (IsAuthenticated, IsAuthor, )