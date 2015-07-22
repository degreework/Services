
from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import UserCreateView, UserDetail, UserUpdate, UserList, GroupViewSet, UserCurrent, UserPassword, RecoveryPassword, RecoveryPassword_confirm, RecoveryPasswordDone


#urls for Updating
routerDetail = UserUpdate.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy',
})

from rest_framework import routers

routerGroups = routers.DefaultRouter()
routerGroups.register(r'groups', GroupViewSet)


routerUser = format_suffix_patterns([
    #url(r'^$', api_root),
    
    #create
    url(r'^$', UserCreateView.as_view({'post': 'create'}), name='user-create'),

    #retrieve, update, destroy
    url(r'^(?P<pk>[0-9]+)$', routerDetail, name='user-update'),

    #detail
    url(r'^detail/(?P<pk>[0-9]+)/$', UserDetail.as_view(), name='user-detail'),

    #get current user
    url(r'^me$', UserCurrent.as_view() , name='user-current'),

    #update passwordrecovery_done
    url(r'^authenticate/(?P<pk>[0-9]+)$', UserPassword.as_view(), name='user-password'),

    #get all asks 
    url(r'^all$', UserList.as_view() , name='user-list'),

    #confirm password
    url(r'^recovery/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', RecoveryPassword_confirm.as_view() , name='password_reset_confirm'),

    #recovery password
    url(r'^recovery$', RecoveryPassword.as_view() , name='recovery-password'),
    
    #recovery done
    url(r'^recovery/done$', RecoveryPasswordDone.as_view() , name='password_reset_done'),

    ])


from rest_framework import routers

routerGroups = routers.DefaultRouter()
routerGroups.register(r'settings', GroupViewSet)
