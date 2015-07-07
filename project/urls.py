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

from users.urls import routerUser, routerGroups
from forum.urls import routerAsk, routerAnswer
from wiki.urls import routerWiki

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^API/users/', include(routerUser)),
    url(r'^API/groups/', include(routerGroups.urls)),
    url(r'^API/auth/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    ##forum
    #url(r'^forum/', include('pybb.urls', namespace='pybb')),
    url(r'^API/forum/ask/', include(routerAsk)),
    #url(r'^API/forum/allAsks/', include(routerAsk)),
    url(r'^API/forum/answer/', include(routerAnswer)),

    url(r'^wiki/', include('waliki.urls')),
    url(r'^API/wiki/', include(routerWiki)),
]
