from django.contrib import admin

from .models import User

admin.site.register(User)

#from django.db.models.loading import get_models
#from django.contrib.auth import models

#get_models(models)[1]._meta.app_label = 'users'