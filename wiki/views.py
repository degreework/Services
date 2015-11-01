import json
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

from waliki.rest.views import (
        PageCreateView as CreateView,
        PageListView as ListView,
        PageRetrieveView as RetrieveView,
        PageEditView as PageEdit,
        PageVersionView
    )

from waliki import views
from waliki.git.views import version as git_version

from waliki.rest.permissions import WalikiPermission_ViewPage

from rest_framework.response import Response
from rest_framework import generics, permissions, status, mixins

from .models import Request, PublicPage, pageComments
from .serializers import RequestSerializer
from .serializers import (
        PageCreateSerializer as CreateSer,
        PageRetrieveSerializer as RetrieveSer,
        PageEditSerializer as PageEditSer,
        PublicPageSerializer
    )


class PageCreateView(CreateView):
    serializer_class = CreateSer


class PageRetrieveView(
    mixins.RetrieveModelMixin,
    generics.GenericAPIView):
    """
    A simple View to retrieve a Page.
    """
    lookup_field = 'slug'
    permission_classes = (WalikiPermission_ViewPage, )

    def get(self, request, *args, **kwargs):
        slug = kwargs['slug']
        response = views.detail(request._request, raw=True, *args, **kwargs)
        
        if 302 ==response.status_code:
            return HttpResponseRedirect(request.path.rstrip('/'+slug)+response.url)
        
        try:
            query = PublicPage.objects.filter(request__page__slug=self.kwargs['slug'])[0]
        except ObjectDoesNotExist:
            raise Http404
        except IndexError:
            raise Http404

        commit = query.request.commit

        version = git_version(request._request, slug=slug, version=commit, raw=True)
        print version
        print "version"
        
        page = query.request.page
        thread = pageComments.objects.get(page=page)

        version = json.loads(version.content)

        response = {
            'id': page.id,
            'thread': thread.id,
            'title': page.title,
            'slug': page.slug,
            'raw': version['raw']
        }

        return Response(response)


class PageEditView(PageEdit):
    serializer_class = PageEditSer
        


class RequestListView(generics.ListAPIView):
    """
    A simple View to list all Request
    """
    serializer_class = RequestSerializer
    #permission_classes = (, )
    paginate_by = 10


    def get_queryset(self):
        return Request.objects.filter(checked=False)

"""
    def get(self, request, *args, **kwargs):
        pages = self.get_queryset()
        return Response(self.get_serializer(pages, many=True).data)
"""

class PageListView(generics.ListAPIView):
    """
    A simple View to list all (Public) Pages
    """
    serializer_class = PublicPageSerializer
    paginate_by = 10

    def get_queryset(self):
        return PublicPage.objects.all()
"""
    def get(self, request, *args, **kwargs):
        pages = self.get_queryset()
        return Response(self.get_serializer(pages, many=True).data)
"""



from django.conf import settings
from reminder.signals import wiki_request_checked

class RequestApproveView(generics.GenericAPIView):
    """
    A simple View to approve a Requet
    """
    #Add permissions
    #permission_classes = (permissions.AllowAny, )

    def post(self, request, slug, version, *args, **kwargs):

        try:
            request_obj = Request.objects.filter(commit=version).reverse()[0]
            
            if request.POST['action'] == "approved":
                request_obj.approve_request(request.user)

                if getattr(settings, 'NOTIFICATIONS', False):
                    wiki_request_checked.send(sender=RequestApproveView, request=request_obj)

                    #from gamification.signals import post_points_wiki
                    #post_points_wiki.send(sender=RequestApproveView, user=request_obj.created_by)
                
                data = {
                    'slug': slug,
                    'version': version,
                    'msg':'Approved',
                    'approved_by': request.user.get_full_name()
                }

                return Response(data, status=status.HTTP_200_OK)
            else:

                request_obj.reject_request(request.user)
                msg = {'msg': 'Contenido rechazado'}

                if getattr(settings, 'NOTIFICATIONS', False):
                    wiki_request_checked.send(sender=RequestApproveView, request=request_obj)
                
                return Response(msg, status=status.HTTP_200_OK)
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