from django.conf.urls import patterns, url

from rest_framework.urlpatterns import format_suffix_patterns

from .views import (
    api_root,
    UserCreateView,
    UserDetail,
    UserUpdate,
    UserList,
    UserCurrent,
    UserStream,
    UserPassword,
    RecoveryPassword,
    password_reset_done,
    password_reset_complete,
    RecoveryPassword_confirm,
    #RecoveryPasswordDone,
    PermissionsCurrentUser )


routerUser = format_suffix_patterns([
    url(r'^$', api_root),
    
    #create
    url(
        r'^new$',
        UserCreateView.as_view({'post': 'create'}),
        name='user_create'
    ),

    #retrieve, update, destroy
    url(
        r'^(?P<pk>[0-9]+)$',
        UserUpdate.as_view({
            'get': 'retrieve',
            'put': 'update',
            'delete': 'destroy',
        }),
        name='user-update'
    ),

    #detail
    url(
        r'^detail/(?P<pk>[0-9]+)/$',
        UserDetail.as_view(),
        name='user-detail'
    ),

    #get current user
    url(
        r'^me$',
        UserCurrent.as_view(),
        name='user-current'
    ),

    #get user stream (wall)
    url(
        r'^wall/(?P<pk>[0-9]+)$',
        UserStream.as_view(),
        name='user-stream'
    ),

    #update passwordrecovery_done
    url(
        r'^authenticate/(?P<pk>[0-9]+)$',
        UserPassword.as_view(),
        name='user-password'),

    #get all users
    url(
        r'^all$',
        UserList.as_view(),
        name='user-list'
    ),

    url(
        r'^permissions/(?P<token>[0-9A-Za-z_\-]+)$',
        PermissionsCurrentUser.as_view(),
        name='permissions-list'
    ),

    #step 1
    url(r'^password/reset/$', 
        #'django.contrib.auth.views.password_reset', 
        RecoveryPassword.as_view(),
        #{'post_reset_redirect' : '/API/users/password/reset/done/'},
        name="password_reset"),
    
    #step 2
    url(r'^password/reset/done/$',
        password_reset_done,
        name="password_reset_done"),

    #step 3
    url(r'^password/reset/(?P<uidb64>[0-9A-Za-z]+)/(?P<token>.+)$', 
        #'django.contrib.auth.views.password_reset_confirm', 
         RecoveryPassword_confirm.as_view(),
        #{'post_reset_redirect' : '/API/users/password/done/'},
        name='password_reset_confirm'),
    
    #step 4
    url(r'^password/done/$',
        #'django.contrib.auth.views.password_reset_complete',
        password_reset_complete,
        name='password_reset_complete'),
    ])