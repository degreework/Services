from django.conf.urls import patterns, url
from waliki.settings import WALIKI_SLUG_PATTERN

from .views import PageCreateView

urlpatterns = patterns('waliki.rest.views',
	url(r'^new$', PageCreateView.as_view() , name='page_new'),
)