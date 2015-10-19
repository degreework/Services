from django.apps import AppConfig
from actstream import registry

class CommentConfig(AppConfig):
    name = 'comment'
    verbose_name = "Comment"

    def ready(self):
        registry.register(
        	self.get_model('Comment'))