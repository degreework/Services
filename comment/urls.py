from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import CommentCreateView, CommentUpdateView, CommentList


"""urls for Comment"""
#urls for Updating
routerCommentDetail = CommentUpdateView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy',
})


routerComment = format_suffix_patterns([
    #url(r'^$', api_root),
    
    #create
    url(r'^$', CommentCreateView.as_view({'post': 'create'}), name='comment-create'),

    #retrieve, update, destroy
    url(r'^(?P<pk>[0-9]+)$', routerCommentDetail, name='acomment-update'),

    #get all asks 
    url(r'^all/(?P<thread>[0-9]+)$', CommentList.as_view() , name='comment-list'),

    ])