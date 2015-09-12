from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns

from .views import (
    ActivitieParentCreateView,
    ActivitieParentUpdateView,
    ActivitieParentListView,

    ActivitieChildCreateView,
    ActivitieChildUpdateCreateView,)


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
    url(r'^$', ActivitieParentCreateView.as_view({'post': 'create'}), name='activitie_parent_create'),

    #retrieve, update, destroy
    url(r'^(?P<pk>[0-9]+)$', routerActivitieParentDetail, name='activitie_parent_update'),

    #listt all activities
    url(r'^all$', ActivitieParentListView.as_view() , name='activitie_parent_list'),
    
	])

"""
Urls for Activitie Child
"""

routerActivitieChildDetail = ActivitieChildUpdateCreateView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy',
})


routerActivitieChild = format_suffix_patterns([
    #url(r'^$', api_root),
    
    #create
    url(r'^$', ActivitieChildCreateView.as_view({'post': 'create'}), name='activitie_child_create'),

    #retrieve, update, destroy
    url(r'^(?P<pk>[0-9]+)$', routerActivitieChildDetail, name='activitie_child_update'),
    
	])
