
from waliki.rest.views import PageCreateView as CreateView
from .serializers import PageCreateSerializer as CreateSer

class PageCreateView(CreateView):
    serializer_class = CreateSer


from rest_framework import generics, permissions
from .models import Request
from .serializers import RequestSerializer

class RequestListView(generics.ListAPIView):
    """
    A simple View to list all Request
    """
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
    permission_classes = (permissions.AllowAny, )
    
