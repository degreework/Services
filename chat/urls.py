from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns

from .views import 


"""
Urls for Activitie Parent
"""
routerActivitieParentDetail = ActivitieParentUpdateView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy',
})

routerActivitieParent = format_suffix_patterns([
    #url(r'^$', api_root),
    
    #create
    #url(r'^new$', ActivitieParentCreateView.as_view({'post': 'create'}), name='activitie_parent_create'),

    #retrieve, update, destroy
    #url(r'^new/(?P<pk>[0-9]+)$', routerActivitieParentDetail, name='activitie_parent_update'),

    #list all activities
    #url(r'^users_connect$', ChatListUsersView.as_view() , name='ChatListUsers'),
    #url(r'^user_chat$', ChatRetrieveUserView.as_view() , name='ChatRetrieveUser'),

    #retreive
    #url(r'^(?P<pk>[0-9]+)$', ActivitieParentReadView.as_view({'get': 'retrieve'}) , name='activitie_parent_retreive'),
    
	])
