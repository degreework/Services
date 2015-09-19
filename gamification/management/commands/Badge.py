from django.core.management.base import BaseCommand, CommandError
from badger.models import Badge
from project.settings import DEFAULT_BADGE_SETTING

class Command(BaseCommand):
    help = 'Create default Badge for users'

    def handle(self, *args, **options):

    	try:
    		Badge(
    			title = DEFAULT_BADGE_SETTING['title'],
    			slug = DEFAULT_BADGE_SETTING['slug'],
    			description = DEFAULT_BADGE_SETTING['description'],
    			image = DEFAULT_BADGE_SETTING['image'], 
    			unique = DEFAULT_BADGE_SETTING['unique'], 
    			nominations_accepted = DEFAULT_BADGE_SETTING['nominations_accepted'], 
    			nominations_autoapproved = DEFAULT_BADGE_SETTING['nominations_autoapproved'],
                points_end = DEFAULT_BADGE_SETTING['points_end']
    			).save()

	        self.stdout.write("Default Badge created")
    	except Exception, e:
    		self.stdout.write("Default Badge can't be created")
    		print e