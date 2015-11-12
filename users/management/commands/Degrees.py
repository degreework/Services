from django.core.management.base import BaseCommand, CommandError
from project.settings import DEFAULT_DEGREE_SETTING
from degree.models import Degree

class Command(BaseCommand):

	def handle(self, *args, **options):
		for degree in DEFAULT_DEGREE_SETTING:
			try:
				Degree(
					code = degree['code'],
					name= degree['name']
					).save()
				self.stdout.write("Default Degrees created")
			except Exception, e:
				self.stdout.write("Default Degrees can't be created")
				raise e

		