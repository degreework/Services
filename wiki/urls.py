from django.conf.urls import patterns, url, include
from waliki.settings import WALIKI_SLUG_PATTERN
from waliki.git.views import WhatchangedFeed

from .views import PageCreateView, RequestListView, PageListView, PageRetrieveView, RequestApproveView, PageVersionView, HistoryListView

from .receivers import *

urlpatterns = patterns('waliki.rest.views',
	#urls for get published wiki
	url(r'^published$', PageListView.as_view() , name='page_published'),

	#urls for wiki create
	url(r'^new$', PageCreateView.as_view() , name='page_new'),

	#urls for request
	url(r'^request/all$', RequestListView.as_view() , name='request_list'),

	#urls for request
	url(r'^history/all$', HistoryListView.as_view() , name='history_list'),


	#urls for approve request
	url(r'^request/approve/(?P<slug>' + WALIKI_SLUG_PATTERN + ')\.\.(?P<version>[0-9a-f\^]{4,40})$', RequestApproveView.as_view() , name='request_approve'),

	#urls for whatchanged in wiki
	url(r'^_whatchanged/rss$', WhatchangedFeed(), name='whatchanged_rss'),

	#get page version
	url(r'^(?P<slug>' + WALIKI_SLUG_PATTERN + ')/version/(?P<version>[0-9a-f\^]{4,40})/$', PageVersionView.as_view(), name='page_version'),
	
	#NOTE: THIS MUST BE LAST URL
	#urls for get a wiki page,
	url(r'^(?P<slug>' + WALIKI_SLUG_PATTERN + ')$', PageRetrieveView.as_view() , name='page_retrieve'),
	
	#url(r'^', include('waliki.rest.urls')),

)