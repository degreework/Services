from django.apps import AppConfig
from actstream import registry

class ModuleConfig(AppConfig):
    name = 'module'
    verbose_name = "Module"

    def ready(self):
        registry.register(
        	self.get_model('Module'),
        	self.get_model('Forum_wrap'),
        	self.get_model('Wiki_wrap'),
        	self.get_model('Quiz_wrap'),
        	self.get_model('Material_wrap'),
        	)