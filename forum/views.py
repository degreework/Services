from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope, TokenHasScope

from .serializers import CreateAskSerializer, UpdateAskSelializer, AnswerCreateSerializer, AnswerUpdateSelializer

"""Classes for Ask"""

class AskCreateView(viewsets.ModelViewSet):
    """
    API endpoint for creating a Ask
    """
    serializer_class = CreateAskSerializer
    permission_classes = (TokenHasReadWriteScope, )

from .models import Ask
from post_framework.permissions import IsAuthor

class AskUpdateView(viewsets.ModelViewSet):
    """
    API endpoint for retrieve, update, destroy a Ask
    """
    queryset = Ask.objects.all()
    serializer_class = UpdateAskSelializer
    permission_classes = (TokenHasReadWriteScope, IsAuthor,)



"""Classes for Answers"""

class AnswerCreateView(viewsets.ModelViewSet):
    """
    API endpoint for creating a Answer
    """
    serializer_class = AnswerCreateSerializer
    permission_classes = (TokenHasReadWriteScope, )

from .models import Answer

class AnswerUpdateView(viewsets.ModelViewSet):
    """
    API endpoint for retrieve, update, destroy a Answer
    """
    queryset = Answer.objects.all()
    serializer_class = AnswerUpdateSelializer
    permission_classes = (TokenHasReadWriteScope, IsAuthor,)