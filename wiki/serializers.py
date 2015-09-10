from waliki.settings import WALIKI_DEFAULT_MARKUP
from waliki import views
from waliki.models import Page
from waliki.signals import page_preedit

from rest_framework import serializers, request

import json

from .models import Request, pageComments
from .signals import page_request

class PageCreateSerializer(serializers.ModelSerializer):
    """
    Serializer Class to create a Page.
    """

    raw = serializers.CharField()
    message = serializers.CharField(write_only=True)
    extra_data = serializers.SerializerMethodField()


    def get_extra_data(self, obj, *args, **kwargs):
        form_extra_data = {}
        page = Page.objects.get(slug=self.context['request'].POST.get('slug'))

        receivers_responses = page_preedit.send(sender=views.edit, page=page)
        for r in receivers_responses:
            if isinstance(r[1], dict) and 'form_extra_data' in r[1]:
                form_extra_data.update(r[1]['form_extra_data'])
        return json.dumps(form_extra_data)
 

    def save(self, *args, **kwargs):
        """call to waliki new function""" 
        #call waliki new function
        mutable = self.context['request'].POST._mutable
        self.context['request'].POST._mutable = True
        self.context['request'].POST['markup'] = WALIKI_DEFAULT_MARKUP
        self.context['request'].POST._mutable = mutable
        response = views.new(self.context['request']._request,*args, **kwargs)


        #if 'extra_data' no comming in payload
        if not self.context['request'].POST.get('extra_data', False):
            mutable = self.context['request'].POST._mutable
            self.context['request'].POST._mutable = True
            self.context['request'].POST['extra_data'] = self.get_extra_data(self.instance)
            ##self.context['request'].POST['markup'] = "markdown"
            self.context['request'].POST._mutable = mutable

        kwargs['slug'] = self.context['request'].POST['slug']

        response = views.edit(self.context['request'],*args, **kwargs)
        ##
        page = Page.objects.filter(slug=kwargs['slug'])[0]

        # para los comentarios
        pageComments.objects.create(page = page)
        
        #Create new reques
        commit = json.loads(self.get_extra_data(self.instance))['parent']
        page_request.send(sender=Request, page=page, commit=commit, author=self.context['request'].user)

        #if user have permissions, then automatic aprove the request
        if self.context['request'].user.has_perm( 'wiki.can_approve_request' ):
            request = Request.objects.filter(commit=commit)[0]
            request.approve_request(self.context['request'].user)


    class Meta():
        model = Page
        fields = ('id', 'title', 'slug', 'raw', 'markup' ,'message', 'extra_data', )
        read_only_fields = ('id', 'markup',)


class PageEditSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer Class to edit a Page.
    """
    raw = serializers.CharField()
    message = serializers.CharField(write_only=True)
    extra_data = serializers.SerializerMethodField()

    def get_extra_data(self, page):
        form_extra_data = {}
        receivers_responses = page_preedit.send(sender=views.edit, page=page)
        for r in receivers_responses:
            if isinstance(r[1], dict) and 'form_extra_data' in r[1]:
                form_extra_data.update(r[1]['form_extra_data'])
        return json.dumps(form_extra_data)


    def save(self, *args, **kwargs):
        """call to waliki edit function"""

        mutable = self.context['request'].POST._mutable
        self.context['request'].POST._mutable = True
        self.context['request'].POST['markup'] = WALIKI_DEFAULT_MARKUP
        self.context['request'].POST._mutable = mutable


        #if 'extra_data' no comming in payload
        if not self.context['request'].POST.get('extra_data', False):
            mutable = self.context['request'].POST._mutable
            self.context['request'].POST._mutable = True
            self.context['request'].POST['extra_data'] = self.get_extra_data(self.instance)
            self.context['request'].POST._mutable = mutable

        kwargs['slug'] = self.instance.slug

        response = views.edit(self.context['request'],*args, **kwargs)

        page = Page.objects.filter(slug=kwargs['slug'])[0]

        #Create new reques
        commit = json.loads(self.get_extra_data(self.instance))['parent']
        page_request.send(sender=Request, page=page, commit=commit, author=self.context['request'].user)


    class Meta():
        model = Page
        fields = ('id', 'title', 'slug', 'raw', 'markup' ,'message', 'extra_data', )
        read_only_fields = ('id', 'slug', )


class PageRetrieveSerializer(serializers.ModelSerializer):
    """
    Serializer Class to retrieve a Page.
    """
    date = serializers.SerializerMethodField()
    id_thread = serializers.SerializerMethodField()

    def get_id_thread(self, obj, *args, **kwargs):
        return pageComments.objects.get(page=obj).id


    def get_date(self, obj, *args, **kwargs):
        #print obj.slug
        #print Request.objects.filter(page=obj)
        return ''

    class Meta():
        model = Page
        fields = ('id', 'title', 'slug', 'raw', 'markup', 'date', 'id_thread' )
        read_only_fields = fields    


class RequestSerializer(serializers.ModelSerializer):

    page = serializers.SerializerMethodField()
    review = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()

    def get_page(self, obj, *args, **kwargs):
        data = {
            'title': obj.page.title,
            'slug': obj.page.slug
        }
        return data

    def get_review(self, obj, *args, **kwargs):
        if obj.approved is True:
            data = {
                'approved': {'is': obj.approved, 'approved_at': obj.approved_at},
                'reviewer' :{
                    'id': obj.approved_by.id,
                    'fullname': obj.approved_by.get_full_name() 
                    }
                }
        else:
            data = {'approved': {'is': obj.approved}}

        return data

    def get_author(self, obj, *args, **kwargs):
        return {'id': obj.created_by.id, 'fullname': obj.created_by.get_full_name(), 'created_at': obj.created_at}

    class Meta():
        model = Request
        fields = ('id', 'page', 'commit', 'review', 'author' )
        read_only_fields = fields



class PublicPageSerializer(RequestSerializer):

    def get_page(self, obj, *args, **kwargs):
        data = {
            'title': obj.request.page.title,
            'slug': obj.request.page.slug
        }
        return data

    def get_review(self, obj, *args, **kwargs):
        if obj.request.approved is True:
            data = {
                'approved': {'is': obj.request.approved, 'approved_at': obj.request.approved_at},
                'reviewer' :{
                    'id': obj.request.approved_by.id,
                    'fullname': obj.request.approved_by.get_full_name() 
                    }
                }
        else:
            data = {'approved': {'is': obj.request.approved}}

        return data

    def get_author(self, obj, *args, **kwargs):
        return {'id': obj.request.created_by.id, 'fullname': obj.request.created_by.get_full_name(), 'created_at': obj.request.created_at}


