# -*- coding: utf-8 -*-

from rest_framework import viewsets, generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Module
from .serializers import ModuleSerializer


class ModuleCreateView(viewsets.ModelViewSet):
    """
    API endpoint for creating a Module
    """
    serializer_class = ModuleSerializer
    permission_classes = (AllowAny, )

class ModuleUpdateView(viewsets.ModelViewSet):
    """
    API endpoint for retrieve, update, destroy a Module
    """
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = (AllowAny, )
    #permission_classes = (TokenHasReadWriteScope, IsAuthor,)

class ModuleReadView(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for retreive an Module
    """
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = (IsAuthenticated, )
    lookup_field = 'slug'


class ModuleListView(generics.ListAPIView):
    """
    View to list all Modules in app
    """

    #authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (AllowAny,)
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    paginate_by = 100


"""Views for Forum wrap"""
from rest_framework.decorators import api_view
from forum.views import AskCreateView
from forum.models import Ask

from .models import Module, Forum_wrap
from django.http import Http404

@api_view(['POST'])
def module_forum_create_wrap(request, module):
    """
    wrap create Ask
    """
    try:
        module = Module.objects.get(slug=module)
        response = AskCreateView.as_view({'post':'create'})(request)
        
        ask = Ask.objects.get(pk=response.data['id'])
        Forum_wrap(module=module, ask=ask).save()
        
        return response

    except Module.DoesNotExist:
        raise Http404

from forum.serializers import ShortAskSerializer
@api_view(['GET'])
def module_forum_all_wrap(request, module):
    """
    wrap listing Ask
    """
    try:
        module = Module.objects.get(slug=module)
        #response = AskCreateView.as_view({'post':'create'})(request)
        
        ask = Forum_wrap.objects.get(module=module)
        print ask
        
        return None

    except Module.DoesNotExist:
        raise Http404


from forum.models import Ask
class ForumList(generics.ListAPIView):
    """
    View to list all aks in the foro.
    """

    #authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (AllowAny,)
    #queryset = Forum_wrap.objects.all()
    serializer_class = ShortAskSerializer
    paginate_by = 10

    def get_queryset(self):
        Query = Module.objects.get(slug=self.kwargs['module'])
        print Query.objects.filter(ask=Forum_wrap.objects.filter(module=module).ask )
        return Forum_wrap.objects.filter(module=module).ask