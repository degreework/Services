from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope, TokenHasScope

from .serializers import PageCreateSerializer, PageUpdateSelializer, PageDetailSerializer, PageListSerializer

from waliki.models import Page

"""Classes for Page from Wiki"""

class PageCreateView(viewsets.ModelViewSet):
    """
    API endpoint for creating a Page
    """
    lookup_field = 'slug'
    serializer_class = PageCreateSerializer
    permission_classes = (AllowAny, )
    #permission_classes = (TokenHasReadWriteScope, )

    def get_queryset(self):
        queryset = Page.objects.all()
        slug = self.request.QUERY_PARAMS.get('slug', None)
        if slug is not None:
            queryset = queryset.filter(slug=slug)
        return queryset


class PageUpdateView(viewsets.ModelViewSet):
    """
    API endpoint for retrieve, update, destroy a Page
    """
    queryset = Page.objects.all()
    serializer_class = PageUpdateSelializer
    permission_classes = (AllowAny, )
    #permission_classes = (TokenHasReadWriteScope, IsAuthor,)

    def get_queryset(self):
        queryset = Page.objects.all()
        slug = self.request.QUERY_PARAMS.get('slug', None)
        if slug is not None:
            queryset = queryset.filter(slug=slug)
        return queryset


from rest_framework.response import Response
from django.shortcuts import get_object_or_404


class PageListView(viewsets.ViewSet):
    """
    A simple ViewSet that for listing or retrieving pages.
    """
    queryset = Page.objects.all()
    serializer_class = PageListSerializer
    permission_classes = (AllowAny, )


    def list(self, request):
        queryset = Page.objects.all()
        serializer = PageListSerializer(queryset, many=True)
        return Response(serializer.data)


class PageDetailView(viewsets.ViewSet):
    """
    A simple ViewSet that for listing or retrieving pages.
    """
    queryset = Page.objects.all()
    serializer_class = PageDetailSerializer
    permission_classes = (AllowAny, )

    def retrieve(self, request, pk=None):
        queryset = Page.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = PageDetailSerializer(user)
        return Response(serializer.data)


from waliki.git import Git
from django.conf import settings
import json

class PageVersionsView(viewsets.ViewSet):
    """
    A simple ViewSet that for listing or retrieving pages.
    """
    queryset = Page.objects.all()
    permission_classes = (AllowAny, )


    def retrieve(self, request, pk=None, pag=1):
        page = get_object_or_404(Page, pk=pk)
        # The argument passed for pag might be a string, but we want to
        # do calculations on it. So we must cast just to be sure.
        pag = int(pag or 1)
        skip = (pag - 1) * settings.WALIKI_PAGINATE_BY
        max_count = settings.WALIKI_PAGINATE_BY
        
        history = Git().history(page)
        max_changes = max([(v['insertion'] + v['deletion']) for v in history])
        data = {'page': PageDetailSerializer(page, many=False).data,
        'history': history[skip:(skip+max_count)],
        'max_changes': max_changes,
        'prev': pag - 1 if pag > 1 else None,
        'next': pag + 1 if skip + max_count < len(history) else None}
        return Response(data)