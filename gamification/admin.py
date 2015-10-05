from django.contrib import admin
from .models import Scores, Votes

class ScoresAdmin(admin.ModelAdmin):
    list_display = ('event', 'id_event', 'score' )

# Register your models here.
admin.site.register(Scores, ScoresAdmin)
admin.site.register(Votes)