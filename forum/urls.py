from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import AskCreateView, AskUpdateView, AskList, AskDetail, AnswerCreateView, AnswerUpdateView, AnswerList


"""urls for Asks"""
#urls for Updating
routerAskDetail = AskUpdateView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy',
})


routerAsk = format_suffix_patterns([
    #url(r'^$', api_root),
    
    #create
    url(r'^$', AskCreateView.as_view({'post': 'create'}), name='ask-create'),

    #retrieve, update, destroy
    url(r'^(?P<pk>[0-9]+)$', routerAskDetail, name='ask-update'),

    #detail
    url(r'^detail/(?P<pk>[0-9]+)$', AskDetail.as_view({'get': 'retrieve'}), name='ask-detail'),

    #get all asks 
    url(r'^all$', AskList.as_view() , name='ask-list'),

    ])


"""urls for Answers"""

#urls for Updating
routerAnswerDetail = AnswerUpdateView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy',
})

routerAnswer = format_suffix_patterns([
    #url(r'^$', api_root),
    
    #create
    url(r'^$', AnswerCreateView.as_view({'post': 'create'}), name='answer-create'),

    #retrieve, update, destroy
    url(r'^(?P<pk>[0-9]+)$', routerAnswerDetail, name='answer-update'),

    #get all answers
    url(r'^all/(?P<pk>[0-9]+)$', AnswerList.as_view() , name='answer-list'),


    ])