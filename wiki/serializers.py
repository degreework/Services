from waliki import views
from waliki.models import Page
from waliki.signals import page_preedit

from rest_framework import serializers, request

import json


class PageCreateSerializer(serializers.ModelSerializer):
    """
    Serializer Class to create a Page.
    """

    raw = serializers.CharField()
    message = serializers.CharField(write_only=True)
    extra_data = serializers.SerializerMethodField()


    def get_extra_data(self, *args, **kwargs):
        form_extra_data = {}
        page = Page.objects.get(slug=self.context['request'].POST.get('slug'))

        receivers_responses = page_preedit.send(sender=views.edit, page=page)
        for r in receivers_responses:
            if isinstance(r[1], dict) and 'form_extra_data' in r[1]:
                form_extra_data.update(r[1]['form_extra_data'])
        return json.dumps(form_extra_data)
 

    def save(self, *args, **kwargs):
        """call to waliki new function"""
        print "MY HACK"
        
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


    class Meta():
        model = Page
        fields = ('id', 'title', 'slug', 'raw', 'markup' ,'message', 'extra_data', )
        read_only_fields = ('id', )
