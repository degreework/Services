from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope, TokenHasScope

from .serializers import *

# Create your views here.

#---------------------------------
#   BADGE
#---------------------------------

class BadgeCreate(viewsets.ModelViewSet):
    serializer_class = BadgeCreateSerializer
    permission_classes = (AllowAny, )


class BadgeDetail(viewsets.ReadOnlyModelViewSet):
    queryset = Badge.objects.all()
    serializer_class = BadgeCreateSerializer
    permission_classes = (AllowAny, )


class BadgeList(generics.ListAPIView):
    queryset = Badge.objects.all()
    serializer_class = BadgeCreateSerializer
    permission_classes = (AllowAny, )


class BadgesUpdateView(viewsets.ModelViewSet):
    queryset = Badge.objects.all()
    serializer_class = BadgeCreateSerializer
    permission_classes = (AllowAny, )


#---------------------------------
#   AWARD
#---------------------------------

class AwardDetail(viewsets.ReadOnlyModelViewSet):
    queryset = Award.objects.all()
    serializer_class = AwardCreateSerializer
    permission_classes = (AllowAny, )


class AwardList(APIView):
    def get(self,*args, **kwargs):
        permission_classes = (AllowAny, )
        user = self.kwargs['pk']
        awards = Award.objects.filter(user = kwargs['pk'])
        serializer = AwardCreateSerializer(awards, many=True)
        return Response(serializer.data)
        


class AwardUpdateView(viewsets.ModelViewSet):
    queryset = Award.objects.all()
    serializer_class = AwardCreateSerializer
    permission_classes = (AllowAny, )


#---------------------------------
#   PROGRESS
#---------------------------------
from badger.models import Progress
from rest_framework.response import Response

class ProgressDetail(APIView):
    
    def get(self,*args, **kwargs):

        permission_classes = (AllowAny, )
        user = self.kwargs['pk']
        progress = Progress.objects.get(user= user)
        serializer = ProgressCreateSerializer(progress)
        return Response(serializer.data)



#---------------------------------
#   Scores
#---------------------------------

class ScoresView(viewsets.ModelViewSet):
    queryset = Scores.objects.all()
    serializer_class = ScoresUpdateSerializer
    permission_classes = (AllowAny, )



#-------------
#  Votes
#
from post_framework.models import Thread
from .models import Votes
class VoteCreateView(viewsets.ModelViewSet):
    """To create a vote"""
    serializer_class = VotesSerializer
    permission_classes = (IsAuthenticated, )


class VoteListView(generics.ListAPIView):
    """To view Thread's votes detail"""
    serializer_class = ListVotesSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return Thread.objects.filter(pk=self.kwargs['pk'])

