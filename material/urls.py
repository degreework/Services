from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns

from .views import (
    MaterialCreateView,
    #MaterialUpdateView,
    MaterialListView,
    MaterialReadView
    )


"""
Urls for Material File

routerMaterialFileDetail = MaterialUpdateView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy',
})
"""
routerMaterial = format_suffix_patterns([
    #url(r'^$', api_root),
    
    #create
    url(r'^new$', MaterialCreateView.as_view({'post': 'create'}), name='material_create'),

    #retrieve, update, destroy
    #url(r'^new/(?P<pk>[0-9]+)$', routerMaterialFileDetail, name='material_update'),

    #list all activities
    url(r'^all$', MaterialListView.as_view() , name='material_list'),

    #retreive
    url(r'^(?P<pk>[0-9]+)$', MaterialReadView.as_view({'get': 'retrieve'}) , name='material_retreive'),
    
	])
