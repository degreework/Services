from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns

from .views import (
    ActivitieParentCreateView,
    ActivitieParentUpdateView,
    ActivitieParentListView,
    ActivitieParentReadView,

    ActivitieChildCreateView,
    ActivitieChildUpdateCreateView,
    ActivitieChildRetreiveView,

    ActivitieChildListView,
    ActivitieChildCheckView,)


"""
Urls for Activitie Parent
"""
routerActivitieParentDetail = ActivitieParentUpdateView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy',
})

from module.settings import MODULE_SLUG_PATTERN

routerActivitieParent = format_suffix_patterns([
    #url(r'^$', api_root),
    
    #create
    url(r'^new$', ActivitieParentCreateView.as_view({'post': 'create'}), name='activitie_parent_create'),

    #retrieve, update, destroy
    url(r'^(?P<slug>'+MODULE_SLUG_PATTERN+')/new/(?P<pk>[0-9]+)$', routerActivitieParentDetail, name='activitie_parent_update'),

    #list all activities
    url(r'^all$', ActivitieParentListView.as_view() , name='activitie_parent_list'),

    #retreive
    url(r'^(?P<pk>[0-9]+)$', ActivitieParentReadView.as_view({'get': 'retrieve'}) , name='activitie_parent_retreive'),
    
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

    #previous
    url(r'^previous/(?P<id>[0-9]+)$', ActivitieChildRetreiveView.as_view(), name='activitie_child_previous'),


    #list all activities
    url(r'^all/(?P<id>[0-9]+)$', ActivitieChildListView.as_view() , name='activitie_child_list'),

    #check
    url(r'^(?P<mod_slug>.+)/check/(?P<id>[0-9]+)$', ActivitieChildCheckView.as_view(), name='activitie_child_check'),
    
	])
