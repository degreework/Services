from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete

from  gamification.signals import createBadgeModule
from .models import Module


from .serializers import ModuleSerializer

@receiver(post_save, sender=Module)
def signal_create_module(sender, instance, using, **kwargs):
	"""
	if a Module is created, Badge must be created too
	"""	
	createBadgeModule.send(sender=ModuleSerializer, module=instance)





from activitie.models import ActivitieParent

@receiver(pre_delete, sender=ActivitieParent)
def signal_delete_activitie(sender, instance, using, **kwargs):
	"""
	if a Activitie is deleted, Badge must be deleted too
	"""	
	#score = Scores.objects.get(id_event=instance.id)
    #print score