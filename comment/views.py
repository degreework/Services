from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope, TokenHasScope

from .models import Comment

from .serializers import CreateCommentSerializer, UpdateCommentSelializer, ShortCommentSerializer

"""Classes for Comment"""

class CommentCreateView(viewsets.ModelViewSet):
    """
    API endpoint for creating a Comment
    """
    serializer_class = CreateCommentSerializer
    permission_classes = (IsAuthenticated, )


from post_framework.permissions import IsAuthor

class CommentUpdateView(viewsets.ModelViewSet):
    """
    API endpoint for retrieve, update, destroy a Comment
    """
    queryset = Comment.objects.all()
    serializer_class = UpdateCommentSelializer
    permission_classes = (IsAuthor, )


from rest_framework.views import APIView
from rest_framework import authentication

class CommentList(generics.ListAPIView):
    """
    View to list all Comment
    """
    serializer_class = ShortCommentSerializer
    permission_classes = (IsAuthenticated, )
    paginate_by = 3

    def get_queryset(self):
        return Comment.objects.filter(parent=self.kwargs['thread'])
