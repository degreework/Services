"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings

from degree.urls import routerDegree
from users.urls import routerUser
from forum.urls import routerAsk, routerAnswer
from wiki.urls import urlpatterns as wiki_url
from comment.urls import routerComment
from comment.urls import routerComment
from servicio.urls import routerQuiz
from servicio.urls import routerQuestions
#from servicio.urls import routerCategory
from activitie.urls import routerActivitieParent, routerActivitieChild
from gamification.urls import routerBadges, routerAward, routerScores, routerVotes

from reminder.urls import *
from module.urls import routerModule
from material.urls import routerMaterial

import notifications

urlpatterns = [
    url(r'^API/degree/', include(routerDegree)),
    url(r'^API/users/', include(routerUser)),
    
    url(r'^API/auth/', include('oauth2_provider.urls', namespace='oauth2_provider')),

    url(r'^API/material/', include(routerMaterial, namespace='material')),
    
    url(r'^API/forum/ask/', include(routerAsk, namespace='forum_ask')),
    url(r'^API/forum/answer/', include(routerAnswer, namespace='forum_answer')),

    url(r'^API/wiki/', include(wiki_url, namespace='wiki')),
    url(r'^API/wiki/', include('waliki.urls')),

    url(r'^API/comment/', include(routerComment, namespace='comment')),
    
    url(r'^API/quiz/', include(routerQuiz, namespace='quiz')),
    url(r'^API/quiz/questions/', include(routerQuestions, namespace='questions')),
    #url(r'^API/quiz/category/', include(routerCategory, namespace='category')),

    url(r'^API/activitie/parent/', include(routerActivitieParent, namespace='activitie_parent')),
    url(r'^API/activitie/', include(routerActivitieChild, namespace='activitie_child')),

    url(r'^API/gamification/', include(routerBadges, namespace='badges')),
    url(r'^API/gamification/', include(routerAward, namespace='award')),
    url(r'^API/gamification/', include(routerScores, namespace='award')),
    url(r'^API/gamification/', include(routerVotes, namespace='votes')),
    #url(r'^API/badges/', include('badger.urls', namespace='badger')),


    url(r'^API/inbox/notifications/', include(routerNotification)),

    url(r'^API/module/', include(routerModule)),


    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

]
