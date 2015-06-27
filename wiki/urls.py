from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import PageCreateView, PageUpdateView, PageDetailView, PageListView, PageVersionsView


"""urls for Asks"""
#urls for Updating

routerPageDetail = PageUpdateView.as_view({
    'get': 'retrieve',
    'post': 'update',
    'delete': 'destroy',
})

from rest_framework.routers import DefaultRouter

#router for List
routerPageList = DefaultRouter()
routerPageList.register(r'list', PageListView)

#router for show
routerPageView = DefaultRouter()
routerPageView.register(r'view', PageDetailView)

#router for Versions
routerPageVersions = DefaultRouter()
routerPageVersions.register(r'history', PageVersionsView)

routerWiki = format_suffix_patterns([
    #url(r'^$', api_root),
    
    #create
    url(r'^$', PageCreateView.as_view({'post': 'create'}), name='wiki-create'),

    #retrieve, update, destroy
    url(r'^(?P<pk>[0-9]+)$', routerPageDetail, name='page-update'),

    ])

routerWiki += routerPageList.urls
routerWiki += routerPageView.urls
routerWiki += routerPageVersions.urls