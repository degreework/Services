from django.core.management.base import BaseCommand, CommandError
from project.settings import DEFAULT_BADGE_SETTING

from gamification.models import Scores

class Command(BaseCommand):
    help = 'Create default Scores'

    def handle(self, *args, **options):

    	try:
			#create Score for wiki
            Scores(id_event=0, score=10, event="Wiki").save()

            self.stdout.write("Default Score created")
        except Exception, e:
    		self.stdout.write("Default Badge can't be created")
    		print e