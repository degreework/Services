from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.conf import settings
from django.shortcuts import get_object_or_404


from rest_framework import viewsets, generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import ActivitieParent, ActivitieChild
from .serializers import ActivitieParentSerializer, ActivitieChildSerializer

from project.permissions import IsTeacher
from .permissions import IsAuthor, CanCreate, CanCheck

class ActivitieParentCreateView(viewsets.ModelViewSet):
    """
    API endpoint for creating an Activitie
    """
    serializer_class = ActivitieParentSerializer
    permission_classes = (IsTeacher, )

from gamification.models import Scores
from  gamification.signals import calculate_points_end_badge
class ActivitieParentUpdateView(viewsets.ModelViewSet):
    """
    API endpoint for updating an Activitie
    """
    queryset = ActivitieParent.objects.all()
    serializer_class = ActivitieParentSerializer
    permission_classes = (IsTeacher, )

    def destroy(self, request, pk, format=None, **kwargs):
        print 'deletio'
        activitie = self.get_object()
        print activitie
        score = Scores.objects.get(id_event=activitie.id)
        print score

        # Se envia la senal para disminuir los puntos con los que se gana la medalla
        badge = kwargs['slug']
        calculate_points_end_badge.send(sender=ActivitieParentUpdateView, author=request.user, badge=badge, points=score.score, action='remove', element='activitie', instance_element=activitie)
        
        # se borra el puntaje y el quiz 
        score.delete()
        activitie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)    



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
        previous = get_object_or_404(ActivitieChild, parent=self.kwargs.get('id', None), author=self.request.user)
        return previous


class ActivitieChildListView(generics.ListAPIView):
    """
    View to list all Activities
    """
    #queryset = ActivitieParent.objects.all()
    #add permission
    permission_classes = (IsTeacher, )
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
                badge = kwargs['mod_slug']
                post_points_activity.send(sender=ActivitieChildCheckView, user=activitie.author, badge = badge, activitie= activitie.parent)
                
                msg['msg'] = 'approved'
                r_status = status.HTTP_200_OK
            
            elif request.POST['action'] == "rejected":
                activitie.do_rejected(request.user)

                
                msg['msg'] = 'rejected'
                r_status = status.HTTP_200_OK

            from reminder.signals import activitie_checked
            if getattr(settings, 'NOTIFICATIONS', False):
                    activitie_checked.send(sender=ActivitieChildCheckView, checker=request.user, activitie=activitie)
            
            return Response(msg, status=r_status)
        except ObjectDoesNotExist, e:
            raise Http404

