
from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import CreateUserView, UserDetail, UserUpdate


#urls for Updating
routerDetail = UserUpdate.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy',
})


routerUser = format_suffix_patterns([
    #url(r'^$', api_root),
    
    #create
    url(r'^$', CreateUserView.as_view({'post': 'create'}), name='user-create'),

    #retrieve, update, destroy
    url(r'^(?P<pk>[0-9]+)/$', routerDetail, name='user-update'),

    #detail
    url(r'^detail/(?P<pk>[0-9]+)/$', UserDetail.as_view(), name='user-detail'),

    ])
