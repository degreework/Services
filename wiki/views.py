from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope, TokenHasScope

from .serializers import PageCreateSerializer, PageUpdateSelializer

"""Classes for Page from Wiki"""

class PageCreateView(viewsets.ModelViewSet):
    """
    API endpoint for creating a Page
    """
    serializer_class = PageCreateSerializer
    permission_classes = (AllowAny, )
    #permission_classes = (TokenHasReadWriteScope, )


from waliki.models import Page

class PageUpdateView(viewsets.ModelViewSet):
    """
    API endpoint for retrieve, update, destroy a Page
    """
    queryset = Page.objects.all()
    serializer_class = PageUpdateSelializer
    permission_classes = (AllowAny, )
    #permission_classes = (TokenHasReadWriteScope, IsAuthor,)

