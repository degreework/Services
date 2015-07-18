
from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import DegreeList

routerDegree = format_suffix_patterns([
    #url(r'^$', api_root),
    #get all asks 
    url(r'^all$', DegreeList.as_view() , name='degree-list'),

    ])