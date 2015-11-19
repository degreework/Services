from django.apps import AppConfig
from actstream import registry

from waliki.models import Page

class WikiConfig(AppConfig):
    name = 'wiki'
    verbose_name = "Wiki"

    def ready(self):
        registry.register(
        	Page,
		self.get_model('PublicPage'),
        	self.get_model('pageComments'),
        	self.get_model('Request'))
