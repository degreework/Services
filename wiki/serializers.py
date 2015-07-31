from waliki import views
from waliki.models import Page
from waliki.signals import page_preedit

from rest_framework import serializers, request

import json

from .models import Request
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
        response = views.new(self.context['request']._request, *args, **kwargs)


        #if 'extra_data' no comming in payload
        if not self.context['request'].POST.get('extra_data', False):
            mutable = self.context['request'].POST._mutable
            self.context['request'].POST._mutable = True
            self.context['request'].POST['extra_data'] = self.get_extra_data(self.instance)
            self.context['request'].POST._mutable = mutable

        kwargs['slug'] = self.context['request'].POST['slug']

        response = views.edit(self.context['request'],*args, **kwargs)
        ##
        page = Page.objects.filter(slug=kwargs['slug'])[0]
        
        #Create new reques
        commit = json.loads(self.get_extra_data(self.instance))['parent']
        page_request.send(sender=Request, page=page, commit=commit)


    class Meta():
        model = Page
        fields = ('id', 'title', 'slug', 'raw', 'markup' ,'message', 'extra_data', )
        read_only_fields = ('id', )


class PageRetrieveSerializer(serializers.ModelSerializer):
    """
    Serializer Class to retrieve a Page.
    """
    date = serializers.SerializerMethodField()

    def get_date(self, obj, *args, **kwargs):
        print obj.slug
        print Request.objects.filter(page=obj)

        return ''


    class Meta():
        model = Page
        fields = ('id', 'title', 'slug', 'raw', 'markup', 'date' )
        read_only_fields = fields    


class RequestSerializer(serializers.ModelSerializer):

    page = serializers.SerializerMethodField()

    def get_page(self, obj, *args, **kwargs):
        data = {
            'title': obj.page.title,
            'slug': obj.page.slug
        }

        return data

    class Meta():
        model = Request
        fields = ('id', 'page', 'commit', 'created', 'approved', 'approved_by' )
        read_only_fields = fields
