from django.contrib import admin

from .models import Request

class RequestAdmin(admin.ModelAdmin):
     list_display = ('id', 'page', 'commit', )

admin.site.register(Request, RequestAdmin)