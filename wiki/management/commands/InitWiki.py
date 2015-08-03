from django.core.management.base import BaseCommand, CommandError

import os

from waliki import settings
from waliki.git import Git

class Command(BaseCommand):
    help = 'Create Super user in db'

    def handle(self, *args, **options):
        try:
            from waliki.settings import WALIKI_DATA_DIR
            content_dir = WALIKI_DATA_DIR
            #content_dir = 'repo'
            os.chdir(content_dir)
            if not os.path.isdir(os.path.join(content_dir, '.git')):
                git.init()
                git.config("user.email", settings.WALIKI_COMMITTER_EMAIL)
                git.config("user.name", settings.WALIKI_COMMITTER_NAME)

            self.stdout.write("Git repo created")
        
        except Exception, e:
            print e
            self.stdout.write("Git repo can't be created")