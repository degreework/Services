from django.conf.urls import patterns, url

from rest_framework.urlpatterns import format_suffix_patterns

from .views import (
    ModuleCreateView,
    ModuleUpdateView,
    ModuleListView,
    ModuleReadView,

    module_forum_create_wrap,
    module_forum_all_wrap,
    ForumList)

from .settings import MODULE_SLUG_PATTERN

"""urls for Module"""
#urls for Updating
routerModuleDetail = ModuleUpdateView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy',
})

routerModule = format_suffix_patterns([
    #url(r'^$', api_root),
    
    #create Module
    url(
        r'^new$',
        ModuleCreateView.as_view({'post': 'create'}),
        name='module-create'
    ),

    #retrieve, update, destroy, Module
    url(
    	r'^new/(?P<pk>[0-9]+)$',
    	routerModuleDetail,
    	name='module-update'
    ),

    url(r'^detail/(?P<slug>'+MODULE_SLUG_PATTERN+')$', ModuleReadView.as_view({'get': 'retrieve'}) , name='module_retreive'),


    #get all Modules
    url(
        r'^all$',
        ModuleListView.as_view(),
        name='module-list'
    ),
    
    #FORUM
    #create
    url(
        r'^(?P<module>' + MODULE_SLUG_PATTERN + ')/forum/new$',
        module_forum_create_wrap,
        name='module-forum-create'
    ),

    #create
    url(
        r'^(?P<module>' + MODULE_SLUG_PATTERN + ')/forum/all$',
        ForumList.as_view(),
        name='module-forum-all'
    ),

    ])