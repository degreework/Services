from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

from waliki.rest.views import (
        PageCreateView as CreateView,
        PageListView as ListView,
        PageRetrieveView as RetrieveView,
        PageVersionView
    )

from rest_framework.response import Response
from rest_framework import generics, permissions, status

from .models import Request
from .serializers import RequestSerializer
from .serializers import (
        PageCreateSerializer as CreateSer,
        PageRetrieveSerializer as RetrieveSer
    )


class PageCreateView(CreateView):
    serializer_class = CreateSer


class PageRetrieveView(RetrieveView):
    serializer_class = RetrieveSer


class RequestListView(ListView):
    """
    A simple View to list all Request
    """
    serializer_class = RequestSerializer
    #permission_classes = (permissions.AllowAny, )

    def get_queryset(self):
        return Request.objects.filter(approved=False)

    def get(self, request, *args, **kwargs):
        pages = self.get_queryset()
        return Response(self.get_serializer(pages, many=True).data)


class PageListView(ListView):
    """
    A simple View to list all Pages
    """
    serializer_class = RequestSerializer

    def get_queryset(self):
        return Request.objects.filter(approved=True)

    def get(self, request, *args, **kwargs):
        pages = self.get_queryset()
        return Response(self.get_serializer(pages, many=True).data)


class RequestApproveView(generics.GenericAPIView):
    """
    A simple View to approve a Requet
    """
    #Add permissions
    #permission_classes = (permissions.AllowAny, )

    def get(self, request, slug, version, *args, **kwargs):
        try:
            Request.objects.get(commit=version).approve_request(request.user)
            data = {
                'slug': slug,
                'version': version,
                'msg':'Approved',
                'approved_by': request.user.get_full_name()
            }
            return Response(data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist, e:
            raise Http404