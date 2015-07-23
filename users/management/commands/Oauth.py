from django.core.management.base import BaseCommand, CommandError

from oauth2_provider.models import Application

from users.models import User

class Command(BaseCommand):
    help = 'Create Ouath application in db'

    def handle(self, *args, **options):

    	try:
    		user = User.objects.get(pk=1)
    		Application(
	    		client_id='W768A6yDuxGU8nEQ3iXOvghKxFfUGOWbHPWGHXQw',
	    		user=user,
	    		client_type='confidential',
	    		authorization_grant_type='password',
	    		client_secret='LHrwNGN13ISnvXpQAn4YW5K5eWqzasICAwsGExdT5rmFTuAAsdpC0sH2JUbuAV3Am5U8zBHWRRYDyY1Vi4yQfILTugxCdrbitubEkyVuPU0bYNbknN8WUETNqkeaCixi',
	    		name='Algoritm').save()
	        self.stdout.write("App algoritm created")
    	except Exception, e:
    		self.stdout.write("App algoritm can't be created")