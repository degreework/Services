from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import AskCreateView, AskUpdateView, AnswerCreateView, AnswerUpdateView


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

    ])