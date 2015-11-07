from django.core.management.base import BaseCommand, CommandError

from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission

from project.settings import DEFAULT_GROUP_NAME


class Command(BaseCommand):
    help = 'Create default Groups with Permissions in db'

    def handle(self, *args, **options):
        self.stdout.write("Creating Groups in settings.DEFAULT_GROUP_NAME")

        try:
            for group in DEFAULT_GROUP_NAME.keys():
                print group
                new_group, created = Group.objects.get_or_create(name=group)

                for permission in DEFAULT_GROUP_NAME[group]:
                    print '\t', permission
                    splited_permission = permission.split(" | ")
                    permission = Permission.objects.get(name=splited_permission[2])
                    new_group.permissions.add(permission)


            self.stdout.write("Default Groups created")
        except Exception, e:
            self.stdout.write("Default Groups can't be created")
            print e