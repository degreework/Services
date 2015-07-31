from django.core.management.base import BaseCommand, CommandError

from users.models import User

class Command(BaseCommand):
    help = 'Create Super user in db'

    def handle(self, *args, **options):

    	try:
    		User.objects.create_superuser(
    			email="",
    			codigo='',
    			first_name='',
    			last_name='',
    			password='')

	        self.stdout.write("Super user created")
    	except Exception, e:
    		self.stdout.write("Super user can't be created")