from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns

import receivers

from .views import *


routerNotification = format_suffix_patterns([
    #url(r'^$', api_root),
  
    url(r'^all$', NotificationAllView.as_view({'get': 'list'}), name='notification'),
    url(r'^unread/$', NotificationUnreadView.as_view({'get': 'list'}), name='unread'),
    url(r'^mark-all-as-read/$', mark_all_as_read, name='mark_all_as_read'),
    url(r'^mark-as-read/(?P<id>[0-9]+)/$', mark_as_read, name='mark_as_read'),
    url(r'^mark-as-unread/(?P<id>[0-9]+)/$', mark_as_unread, name='mark_as_unread'),
    url(r'^delete/(?P<id>[0-9]+)$', delete, name="delete"),

    ])