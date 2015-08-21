from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Permission

class Command(BaseCommand):
    help = 'Show a list of all Permissions'

    def handle(self, *args, **options):

        try:
            p = Permission.objects.all()
            for pp in p:
                print pp
                
        except Exception, e:
            self.stdout.write("List Permissions can't be showed")


