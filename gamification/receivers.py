from django.dispatch import receiver

from django.db.models.signals import post_save

from servicio.serializers import Sitting_Serializer
from users.serializers import CreateUserSerializer

from module.serializers import ModuleSerializer

from badger.models import Badge, Award, Progress
from quiz.models import Sitting, Quiz

from .models import Scores

from badger.signals import badge_was_awarded, badge_will_be_awarded
from  .signals import createBadgeModule, post_points_quiz, post_points_wiki, post_points_activity ,calculate_points_end_badge

from badger.utils import get_badge

#------------------------------------------
# crea el progreso de la insignia con la cual inicia el usuario
"""

@receiver(set_progress_user, sender = CreateUserSerializer)
def progress_user_registered(sender, user, **kwargs):
	print 'progress init'
	badge = get_badge('slug')
	progress = badge.progress_for(user)
	progress.save()
"""
	
# crea una medalla por cada modulo que se crea 
@receiver(createBadgeModule, sender = ModuleSerializer)
def badgeModule(sender, module, **kwargs):
	print 'entro badgeModule'
	badge = Badge(title= module.name, slug = module.slug, description = module.description, unique = True)
	badge.save()



@receiver(calculate_points_end_badge)
def points_end_badge(sender, badge, points, **kwargs):
	print 'points_end_badge'
	b = get_badge(badge)
	b.points_end += points
	b.save()




#-------------------------------------------
# funcion para asignar los puntos
def set_points(progress, points):
	
	# si es menor que 100 aumenta los puntos 
	# si es mayor asigna una nueva medalla de ser el caso

	if progress.percent < 100.0:
		progress.increment_by(points)
		progress.update_percent2()
		progress.save()

# de aqui para abajo acomodar notificaciones 
		if progress.percent >= 100:
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
def set_points_quiz(sender, sitting, badge, **kwargs):
	
	if sitting.check_if_passed == True:
		print 'puntos quices'
		
		b = get_badge(badge)
		p = b.progress_for(sitting.user)

		#
		points = Scores.objects.get(id_event=sitting.quiz.id)
		#p = Progress.objects.get( user = sitting.user)
		set_points(p, points.score)
			

from wiki.views import RequestApproveView

# puntos de la wiki  
@receiver(post_points_wiki, sender=RequestApproveView)
def set_points_wiki(sender, user, badge, **kwargs):
	print 'hola puntos de la wiki'
	print user
	b = get_badge(badge)
	p = b.progress_for(user)
	#p = Progress.objects.get( user = user)
	set_points(p)
	

from activitie.views import ActivitieChildCheckView

# puntos de las actvidades  
@receiver(post_points_activity, sender = ActivitieChildCheckView)
def set_points_activitie(sender, user, badge, activitie, **kwargs):
	print 'set_points_activitie'
	b = get_badge(badge)
	p = b.progress_for(user)

	points = Scores.objects.get(id_event=activitie)
	#p = Progress.objects.get( user = user)
	set_points(p, points.score)
