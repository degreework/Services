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
    permission_classes = (AllowAny, )

from .models import Ask
from post_framework.permissions import IsAuthor

class AskUpdateView(viewsets.ModelViewSet):
    """
    API endpoint for retrieve, update, destroy a Ask
    """
    queryset = Ask.objects.all()
    serializer_class = UpdateAskSelializer
    permission_classes = (TokenHasReadWriteScope, IsAuthor,)


from rest_framework.views import APIView
from rest_framework import authentication

class AskList(generics.ListAPIView):
    """
    View to list all aks in the foro.
    """

    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (AllowAny,)
    queryset = Ask.objects.all()
    serializer_class = ShortAskSerializer
    paginate_by = 10


class AskDetail(viewsets.ReadOnlyModelViewSet):
    """
    View to list all aks in the foro.
    """

    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (AllowAny,)
    queryset = Ask.objects.all()
    serializer_class = AskDetailSerializer


"""Classes for Answers"""

class AnswerCreateView(viewsets.ModelViewSet):
    """
    API endpoint for creating a Answer
    """
    serializer_class = AnswerCreateSerializer
    #permission_classes = (TokenHasReadWriteScope, )
    permission_classes = (AllowAny,)

from .models import Answer

class AnswerUpdateView(viewsets.ModelViewSet):
    """
    API endpoint for retrieve, update, destroy a Answer
    """
    queryset = Answer.objects.all()
    serializer_class = AnswerUpdateSelializer
    permission_classes = (TokenHasReadWriteScope, IsAuthor,)



class AnswerList(generics.ListAPIView):
    """
    View to list all aks in the foro.
    """

    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (AllowAny,)
    queryset = Answer.objects.all()
    serializer_class = AnswerShortSerializer
    paginate_by = 10