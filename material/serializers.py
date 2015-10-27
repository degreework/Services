from rest_framework import serializers

from .models import Material, MaterialFile, MaterialLink


class MaterialFileSerializer(serializers.ModelSerializer):
    class Meta():
        model = MaterialFile
        fields = ('id', 'title', 'description', 'file')


class MaterialLinkSerializer(serializers.ModelSerializer):
    class Meta():
        model = MaterialLink
        fields = ('id', 'title', 'description', 'url')


class MaterialListSerializer(serializers.ModelSerializer):
    class Meta():
        model = Material
        fields = ('id', 'title', 'description')


class MaterialSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField()

    def get_content(self, obj, *args, **kwargs):
        content = {}

        if isinstance(obj, MaterialLink):
            content['type'] = 'link'
            content['url'] = obj.url

        elif isinstance(obj, MaterialFile):
            content['type'] = 'file'
            content['url'] = obj.file.url

        return content

    class Meta():
        model = Material
        fields = ('id', 'title', 'description', 'content')