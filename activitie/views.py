from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import get_object_or_404


from rest_framework import viewsets, generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import ActivitieParent, ActivitieChild
from .serializers import ActivitieParentSerializer, ActivitieChildSerializer

from .permissions import IsAuthor, CanCreate, CanCheck

class ActivitieParentCreateView(viewsets.ModelViewSet):
    """
    API endpoint for creating an Activitie
    """
    serializer_class = ActivitieParentSerializer
    permission_classes = (CanCreate, )


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


class ActivitieParentReadView(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for retreive an Activitie
    """
    queryset = ActivitieParent.objects.all()
    serializer_class = ActivitieParentSerializer
    permission_classes = (IsAuthenticated, )
    



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


class ActivitieChildRetreiveView(generics.RetrieveAPIView):
    """
    API endpoint for retreive a previous Activitie
    """
    queryset = ActivitieChild.objects.all()
    serializer_class = ActivitieChildSerializer
    permission_classes = (IsAuthenticated, IsAuthor, )
    lookup_field = 'id'

    def get_queryset(self):
        print "quwey"
        print self.kwargs.get('id', None)
        previous = get_object_or_404(ActivitieChild, parent=self.kwargs.get('id', None), author=self.request.user)
        print previous
        return previous


class ActivitieChildListView(generics.ListAPIView):
    """
    View to list all Activities
    """
    queryset = ActivitieParent.objects.all()
    #add permission
    permission_classes = (IsAuthenticated, )
    serializer_class = ActivitieChildSerializer
    paginate_by = 5

    def get_queryset(self):
        parent = get_object_or_404(ActivitieParent, pk=self.kwargs.get('id', None))
        return ActivitieChild.objects.filter(parent=parent)


class ActivitieChildCheckView(generics.GenericAPIView):
    """
    A simple View to check a Activitie
    """
    #Add permissions
    permission_classes = (CanCheck, )
    serializer_class = ActivitieChildSerializer

    def post(self, request, id, *args, **kwargs):
        try:
            activitie = get_object_or_404(ActivitieChild, id=id)
            msg = {}
            msg['id'] = activitie.id
            r_status = status.HTTP_400_BAD_REQUEST
            
            if request.POST['action'] == "approved":
                activitie.do_approved(request.user)

                #if getattr(settings, 'NOTIFICATIONS', False):
                    #wiki_request_checked.send(sender=RequestApproveView, request=request_obj)

                # puntos actividad
                from gamification.signals import post_points_activity
                post_points_activity.send(sender=ActivitieChildCheckView, user=activitie.author)
                
                msg['msg'] = 'approved'
                r_status = status.HTTP_200_OK
            
            elif request.POST['action'] == "rejected":
                activitie.do_rejected(request.user)

                #if getattr(settings, 'NOTIFICATIONS', False):
                    #wiki_request_checked.send(sender=RequestApproveView, request=request_obj)
                msg['msg'] = 'rejected'
                r_status = status.HTTP_200_OK
            
            return Response(msg, status=r_status)
        except ObjectDoesNotExist, e:
            raise Http404

