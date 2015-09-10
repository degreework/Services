from django.contrib import admin

from .models import Request, pageComments, PublicPage

class RequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'page', 'commit', 'created_at', 'approved',)


class PublicPageAdmin(admin.ModelAdmin):
    list_display = ('page', 'created_by', 'approved_by', 'approved_at')

    def page(self, obj):
        return ("%s" % obj.request.page.title)

    def created_by(self, obj):
    	return ("%s" % obj.request.created_by)

    def approved_by(self, obj):
    	return ("%s" % obj.request.approved_by)

    def approved_at(self, obj):
    	return ("%s" % obj.request.approved_at)

admin.site.register(Request, RequestAdmin)
admin.site.register(pageComments)
admin.site.register(PublicPage, PublicPageAdmin)