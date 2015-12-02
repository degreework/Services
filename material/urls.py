from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns

from .views import (
    MaterialFileCreateView,
    MaterialFileUpdateView,

    MaterialLinkCreateView,
    MaterialLinkUpdateView,
    
    MaterialListView,
    MaterialReadView
    )


"""
Urls for update Material File
"""
routerMaterialFileDetail = MaterialFileUpdateView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy',
})


"""
Urls for update Material Link
"""
routerMaterialLinkDetail = MaterialLinkUpdateView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy',
})

routerMaterial = format_suffix_patterns([
    #url(r'^$', api_root),
    
    #create
    url(r'^f/new$', MaterialFileCreateView.as_view({'post': 'create'}), name='material_create'),
    url(r'^l/new$', MaterialLinkCreateView.as_view({'post': 'create'}), name='material_create'),

    #retrieve, update, destroy
    url(r'^f/new/(?P<pk>[0-9]+)$', routerMaterialFileDetail, name='material_file_update'),
    
    #retrieve, update, destroy
    url(r'^l/new/(?P<pk>[0-9]+)$', routerMaterialLinkDetail, name='material_link_update'),

    
    #list all activities
    url(r'^all$', MaterialListView.as_view() , name='material_list'),

    #retreive
    url(r'^(?P<pk>[0-9]+)$', MaterialReadView.as_view({'get': 'retrieve'}) , name='material_retreive'),
    
	])
