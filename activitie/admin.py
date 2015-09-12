from django.contrib import admin

from .models import ActivitieParent, ActivitieChild

admin.site.register(ActivitieParent)
admin.site.register(ActivitieChild)
