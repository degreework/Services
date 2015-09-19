from rest_framework import viewsets, generics
from rest_framework import status
from rest_framework.mixins import ListModelMixin

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
from notifications.models import Notification
from django.conf import settings

from rest_framework.decorators import api_view, permission_classes

from .serializers import NotificationSerializer
from .permissions import IsRecipient

class NotificationAllView(viewsets.GenericViewSet, ListModelMixin):
    """
    API endpoint for retrieve, update, destroy a Notification
    """
    permission_classes = (IsAuthenticated, IsRecipient, )
    serializer_class = NotificationSerializer
    paginate_by = 5

    def get_queryset(self):
        if getattr(settings, 'NOTIFICATIONS_SOFT_DELETE', False):
            qs = self.request.user.notifications.active()
        else:
            qs = self.request.user.notifications.all()
        return qs


class NotificationUnreadView(viewsets.GenericViewSet, ListModelMixin):
    """
    API endpoint for retrieve, update, destroy a Notification
    """
    permission_classes = (IsAuthenticated, IsRecipient, )
    serializer_class = NotificationSerializer
    paginate_by = 5

    def get_queryset(self):
        return self.request.user.notifications.unread()


@api_view(('DELETE',))
@permission_classes((IsAuthenticated, IsRecipient ))
def delete(request, id):
    notification = get_object_or_404(Notification, recipient=request.user, id=id)
    if getattr(settings, 'NOTIFICATIONS_SOFT_DELETE', False):
        notification.deleted = True
        notification.save()
    else:
        notification.delete()
    
    return Response(status.HTTP_204_NO_CONTENT)


@api_view(('PUT',))
@permission_classes((IsAuthenticated, IsRecipient ))
def mark_all_as_read(request):
    request.user.notifications.mark_all_as_read()
    return Response(status.HTTP_200_OK)


@api_view(('PUT',))
@permission_classes((IsAuthenticated, IsRecipient ))
def mark_as_read(request, id):
    notification = get_object_or_404(Notification, recipient=request.user, id=id)
    notification.mark_as_read()
    return Response(status.HTTP_200_OK)



@api_view(('PUT',))
@permission_classes((IsAuthenticated, IsRecipient ))
def mark_as_unread(request, id):
    notification = get_object_or_404(Notification, recipient=request.user, id=id)
    notification.mark_as_unread()
    return Response(status.HTTP_200_OK)