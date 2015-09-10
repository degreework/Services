from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

from waliki.rest.views import (
        PageCreateView as CreateView,
        PageListView as ListView,
        PageRetrieveView as RetrieveView,
        PageEditView as PageEdit,
        PageVersionView
    )

from rest_framework.response import Response
from rest_framework import generics, permissions, status

from .models import Request, PublicPage
from .serializers import RequestSerializer
from .serializers import (
        PageCreateSerializer as CreateSer,
        PageRetrieveSerializer as RetrieveSer,
        PageEditSerializer as PageEditSer,
        PublicPageSerializer
    )


class PageCreateView(CreateView):
    serializer_class = CreateSer


class PageRetrieveView(RetrieveView):
    serializer_class = RetrieveSer

class PageEditView(PageEdit):
    serializer_class = PageEditSer
        


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
    A simple View to list all (Public) Pages
    """
    serializer_class = PublicPageSerializer

    def get_queryset(self):
        return PublicPage.objects.all()

    def get(self, request, *args, **kwargs):
        pages = self.get_queryset()
        return Response(self.get_serializer(pages, many=True).data)


class RequestApproveView(generics.GenericAPIView):
    """
    A simple View to approve a Requet
    """
    #Add permissions
    #permission_classes = (permissions.AllowAny, )

    def post(self, request, slug, version, *args, **kwargs):
        print("rejected")
        print(request.POST)
        try:
            if request.POST['action'] == "approved":
                Request.objects.get(commit=version).approve_request(request.user)
                msg = {'msg': 'Contenido aprobado'}
                data = {
                    'slug': slug,
                    'version': version,
                    'msg':'Approved',
                    'approved_by': request.user.get_full_name()
                }
                return Response((msg,data), status=status.HTTP_200_OK)
            else:
                Request.objects.get(commit=version).delete()
                msg = {'msg': 'Contenido rechazado'}
                return Response(msg, status.HTTP_200_OK)
        except ObjectDoesNotExist, e:
            raise Http404



class HistoryListView(ListView):
    """
    A simple View to list all Request
    """
    serializer_class = RequestSerializer
    #permission_classes = (permissions.AllowAny, )

    def get_queryset(self):
        return Request.objects.filter(approved=True)

    def get(self, request, *args, **kwargs):
        pages = self.get_queryset()
        return Response(self.get_serializer(pages, many=True).data)