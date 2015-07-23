from django.conf.urls import patterns, url
from waliki.settings import WALIKI_SLUG_PATTERN

from .views import PageCreateView, RequestListView

from .receivers import *

urlpatterns = patterns('waliki.rest.views',
	#urls for wiki
	url(r'^new$', PageCreateView.as_view() , name='page_new'),
	
	#urls for request
	url(r'^request/all$', RequestListView.as_view() , name='request_list'),

)