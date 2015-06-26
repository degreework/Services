from rest_framework import serializers

from waliki.models import Page
from waliki import views

#from django.db import IntegrityError
#from django.core.exceptions import PermissionDenied


class PageCreateSerializer(serializers.ModelSerializer):
    """
    Serializer Class to create Page Wiki
    """
    
    def save(self):
        """call to waliki new function"""
        views.new(self.context['request'])

    class Meta():
        model = Page
        fields = ('title', 'slug', 'markup')

from waliki.signals import page_saved, page_preedit, page_moved

class PageUpdateSelializer(serializers.ModelSerializer):
    """
    Serializer class to update a Page from wiki
    """
    raw = serializers.CharField()
    extra_data = serializers.SerializerMethodField()
    #extra_data = serializers.DictField(child=serializers.SerializerMethodField('get_extra_data'))

    def save(self):
        """call to waliki edit function"""
        print 'save'
        print self.context['request']
        slug = self.context['view'].get_object().slug
        views.edit(self.context['request'], slug)

    def get_extra_data(self, obj):
        return {
            'message': '',
            'parent': page_preedit.send(sender=None, page=obj)[0][1]['form_extra_data']['parent'],
            }


    class Meta():
        model = Page
        fields = ('title', 'markup', 'slug', 'raw', 'extra_data')
        read_only_fields = ('slug',)


#extra_data:{"parent": "715377a"}
