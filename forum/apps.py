from django.apps import AppConfig
from actstream import registry


class ForumConfig(AppConfig):
    name = 'forum'
    verbose_name = "Forum"

    def ready(self):
        registry.register(self.get_model('Ask'), self.get_model('Answer'))