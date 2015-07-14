from rest_framework import serializers

from waliki.models import Page
from waliki import views

#from django.db import IntegrityError
#from django.core.exceptions import PermissionDenied


class PageCreateSerializer(serializers.ModelSerializer):
    """
    Serializer Class to create Page Wiki
    """
    id = serializers.SerializerMethodField()
    raw = serializers.SerializerMethodField()
    #extra_data = serializers.SerializerMethodField()
    
    def save(self):
        """call to waliki new function"""
        #call waliki new page
        views.new(self.context['request'])
        
        slug = self.context['request'].POST['slug']
        #call waliki page edition
        views.edit(self.context['request'], slug)


    def get_id(self, obj):
        return Page.objects.get(slug=obj['slug']).id

    """
    def get_extra_data(self, obj):
        print "get extra_data"
        return {
            'message': '',
            'parent': page_preedit.send(sender=None, page=obj)[0][1]['form_extra_data']['parent'],
            }
    """

    def get_raw(self, obj):
        return self.context['request'].POST['raw']

    class Meta():
        model = Page
        fields = ('id', 'title', 'slug', 'raw', )
        read_only_fields = ('id', )


from waliki.signals import page_saved, page_preedit, page_moved

class PageUpdateSelializer(serializers.ModelSerializer):
    """
    Serializer class to update a Page from wiki
    """
    raw = serializers.SerializerMethodField()
    extra_data = serializers.SerializerMethodField()
    #extra_data = serializers.DictField(child=serializers.SerializerMethodField('get_extra_data'))

    def save(self):
        """call to waliki edit function"""
        slug = self.context['view'].get_object().slug
        views.edit(self.context['request'], slug)

    def get_extra_data(self, obj):
        return {
            'message': '',
            'parent': page_preedit.send(sender=None, page=obj)[0][1]['form_extra_data']['parent'],
            }

    def get_raw(self, obj):
        try:
            raw = self.context['request'].POST['raw']
        except Exception, e:
            raw = ''
        return raw


    class Meta():
        model = Page
        fields = ('id', 'title', 'slug', 'raw', 'extra_data')
        read_only_fields = ('slug',)
        #extra_kwargs = {'raw': {'write_only': True}}


class PageListSerializer(serializers.ModelSerializer):
    """
    Serializer class to show list of Pages
    """

    class Meta():
        model = Page
        fields = ('id', 'title', 'slug', )
        read_only_fields = ('id', 'title', 'slug', )


class PageDetailSerializer(serializers.ModelSerializer):
    """
    Serializer class to show list of Answer
    """
    parent = serializers.SerializerMethodField()

    def get_parent(self, obj):
        return page_preedit.send(sender=None, page=obj)[0][1]['form_extra_data']['parent']


    class Meta():
        model = Page
        fields = ('id', 'title', 'slug', 'raw', 'parent')
        read_only_fields = ('id', 'title', 'slug', 'raw', 'parent')
