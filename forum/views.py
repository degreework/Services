from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope, TokenHasScope

from .serializers import CreateAskSerializer, UpdateAskSelializer, AnswerCreateSerializer, AnswerUpdateSelializer, ShortAskSerializer, AnswerShortSerializer, AskDetailSerializer

"""Classes for Ask"""

class AskCreateView(viewsets.ModelViewSet):
    """
    API endpoint for creating a Ask
    """
    serializer_class = CreateAskSerializer
    permission_classes = (IsAuthenticated, )

from .models import Ask
from post_framework.permissions import IsAuthor

class AskUpdateView(viewsets.ModelViewSet):
    """
    API endpoint for retrieve, update, destroy a Ask
    """
    queryset = Ask.objects.all()
    serializer_class = UpdateAskSelializer
    permission_classes = (IsAuthor, )


from rest_framework.views import APIView
from rest_framework import authentication

class AskList(generics.ListAPIView):
    """
    View to list all aks in the foro.
    """

    queryset = Ask.objects.all()
    serializer_class = ShortAskSerializer
    
    permission_classes = (IsAuthenticated,)
    #authentication_classes = (authentication.TokenAuthentication,)
    paginate_by = 10


class AskDetail(viewsets.ReadOnlyModelViewSet):
    """
    View to list all aks in the foro.
    """

    queryset = Ask.objects.all()
    serializer_class = AskDetailSerializer
    
    permission_classes = (IsAuthenticated,)
    #authentication_classes = (authentication.TokenAuthentication,)


"""Classes for Answers"""
from .models import Answer

class AnswerCreateView(viewsets.ModelViewSet):
    """
    API endpoint for creating a Answer
    """
    serializer_class = AnswerCreateSerializer
    
    permission_classes = (IsAuthenticated, )
    #permission_classes = (TokenHasReadWriteScope, )


class AnswerUpdateView(viewsets.ModelViewSet):
    """
    API endpoint for retrieve, update, destroy a Answer
    """
    queryset = Answer.objects.all()
    serializer_class = AnswerUpdateSelializer
    
    permission_classes = (IsAuthor, )
    #permission_classes = (TokenHasReadWriteScope, IsAuthor,)


from django.shortcuts import get_object_or_404
class AnswerList(generics.ListAPIView):
    """
    View to list all aks in the foro.
    """
    #lookup_field = 'ask'

    serializer_class = AnswerShortSerializer
    
    #authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (IsAuthenticated, )
    paginate_by = 10

    def get_queryset(self):
        return Answer.objects.filter(ask = self.kwargs['pk'])
        #print self.objects.filter(ask = )
