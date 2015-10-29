from django.apps import AppConfig
from actstream import registry

class ActivitieConfig(AppConfig):
    name = 'activitie'
    verbose_name = "Activitie"

    def ready(self):
        registry.register(
        	self.get_model('ActivitieParent'),
        	self.get_model('ActivitieChild')
        	)