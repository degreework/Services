from django.conf.urls import url

from rest_framework.urlpatterns import format_suffix_patterns

from .views import DegreeList

routerDegree = format_suffix_patterns([
    #get all degree
    url(r'^all$', DegreeList.as_view() , name='degree-list'),
])