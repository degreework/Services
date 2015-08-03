from django.contrib import admin

from .models import Ask, Answer

class AskAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'title', )

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'ask', )

admin.site.register(Ask, AskAdmin)
admin.site.register(Answer, AnswerAdmin)
