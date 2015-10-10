from django.contrib import admin

from .models import ActivitieParent, ActivitieChild

class ActivitieChildAdmin(admin.ModelAdmin):
    readonly_fields = ('sent_at', )

admin.site.register(ActivitieParent)
admin.site.register(ActivitieChild, ActivitieChildAdmin)
