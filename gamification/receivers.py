from django.dispatch import receiver

from django.db.models.signals import post_save

from servicio.serializers import Sitting_Serializer

from badger.models import Badge, Award, Progress
from quiz.models import Sitting, Quiz

from badger.signals import badge_was_awarded, badge_will_be_awarded
from  .signals import post_points_quiz, post_points_wiki, post_points_activity

"""
@receiver(badge_will_be_awarded)
def my_callback(sender, **kwargs):
	award = kwargs['award']


@receiver(badge_was_awarded)
def my_callback2(sender, **kwargs):
	award = kwargs['award']

"""
#------------------------------------------
# puntos del quiz 
@receiver(post_points_quiz, sender=Sitting_Serializer)
def set_points_quiz(sender, sitting, **kwargs):
	print 'kwargs'
	print kwargs
	print 'kwargs'
	print sitting
	print sitting.check_if_passed
	if sitting.complete == True:
		print 'entro'
		p = Progress.objects.get( user = sitting.user)
		p.increment_by(10)
		p.update_percent2()
		p.save()



from wiki.views import RequestApproveView

# puntos de la wiki  
@receiver(post_points_wiki, sender=RequestApproveView)
def set_points_wiki(sender, user, **kwargs):
	print 'hola puntos de la wiki'
	print user

"""

# puntos de las actvidades  
@receiver(post_points_activity)
def set_points_quiz(sender, **kwargs):
	print 'hola'

"""