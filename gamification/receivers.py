from django.dispatch import receiver

from django.db.models.signals import post_save

from servicio.serializers import Sitting_Serializer
from users.serializers import CreateUserSerializer

from badger.models import Badge, Award, Progress
from quiz.models import Sitting, Quiz

from badger.signals import badge_was_awarded, badge_will_be_awarded
from  .signals import post_points_quiz, post_points_wiki, post_points_activity, set_progress_user


#------------------------------------------
# crea el progreso de la insignia con la cual inicia el usuario
from badger.utils import get_badge
@receiver(set_progress_user, sender = CreateUserSerializer)
def progress_user_registered(sender, user, **kwargs):
	print 'progress init'
	badge = get_badge('slug')
	progress = badge.progress_for(user)
	progress.save()
	
#-------------------------------------------
# funcion para asignar los puntos
def set_points(progress):
	
	# si es menor que 100 aumenta los puntos 
	# si es mayor asigna una nueva medalla de ser el caso

	if progress.percent < 100.0:
		progress.increment_by(10)
		progress.update_percent2()
		progress.save()
	else:
		#lista todas las medallas 
		badges = list(Badge.objects.order_by('prerequisites').all())
		#medalla del usuario recien asignada
		badge_user =  progress.badge 
		# indice de la medalla en la lista 
		i = badges.index(badge_user)
		# se pasa a la siguiente medalla si existe 
		if i <= len(badges)-1:
			progress.percent = 0
			progress.counter = 0
			progress.badge = badges[i+1]
			progress.save()


# puntos del quiz 
@receiver(post_points_quiz, sender=Sitting_Serializer)
def set_points_quiz(sender, sitting, **kwargs):
	
	if sitting.check_if_passed == True:
		print 'puntos quices'
		
		p = Progress.objects.get( user = sitting.user)
		set_points(p)
			

from wiki.views import RequestApproveView

# puntos de la wiki  
@receiver(post_points_wiki, sender=RequestApproveView)
def set_points_wiki(sender, user, **kwargs):
	print 'hola puntos de la wiki'
	print user
	p = Progress.objects.get( user = user)
	set_points(p)
	

from activitie.views import ActivitieChildCheckView

# puntos de las actvidades  
@receiver(post_points_activity, sender = ActivitieChildCheckView)
def set_points_activitie(sender, user, **kwargs):
	print 'set_points_activitie'
	p = Progress.objects.get( user = user)
	set_points(p)
