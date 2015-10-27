from django.dispatch import receiver

from django.db.models.signals import post_save

from servicio.serializers import Sitting_Serializer
from users.serializers import CreateUserSerializer

from module.serializers import ModuleSerializer

from badger.models import Badge, Award, Progress
from quiz.models import Sitting, Quiz
from activitie.models import ActivitieChild
from .models import Scores



from badger.signals import badge_was_awarded, badge_will_be_awarded
from  .signals import createBadgeModule, post_points_quiz, post_points_wiki, post_points_activity ,calculate_points_end_badge

from reminder.signals import gamification_badge_award

from badger.utils import get_badge
from actstream import action



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


def verify_remove_for_award(badge):
	print 'verify_remove_for_award'
	# se traen todas las medallas asignadas
	awards = Award.objects.filter(badge=badge)
	# se eliminan las tuplas de medallas asignadas ya que hay mas material
	awards.delete()

	progress = Progress.objects.filter(badge=badge)
	for item in progress:
		set_points(item, 0, badge, item.user)


def verify_users_for_award(badge, element, instance_element): # estoy probando este
	print 'verify_users_for_award'
	print instance_element.id

	progress = Progress.objects.filter(badge=badge)
	for item in progress:

		if badge.points_end > 0 and element == 'quiz':

			sitting = Sitting.objects.filter(quiz = instance_element, user = item.user, complete = True, check_if_passed = True)
			if len(sitting) > 0:
				points = Scores.objects.get(id_event = instance_element.id)
				item.counter -= points.score
				item.update_percent2()
				item.save()  
				if item.percent >= 100:
					gamification_badge_award.send(sender = set_points, badge = badge, user = item.user)
					#action.send(user, verb='badge', action_object=badge, target=badge)
			else:	
				set_points(item, 0, badge, item.user)

		elif badge.points_end >0 and element == 'activitie':
			
			activitie_child = ActivitieChild.objects.filter(parent = instance_element, author = item.user, status = 3)
			if len(activitie_child)>0:
				points = Scores.objects.get(id_event = instance_element.id)
				item.counter -= points.score
				item.update_percent2()
				item.save()
				if item.percent >= 100:
					gamification_badge_award.send(sender = set_points, badge = badge, user = item.user)
					#action.send(user, verb='badge', action_object=badge, target=badge)  
				
			else:
				set_points(item, 0, badge, item.user)
		else:
			item.counter = 0
			item.percent = 0
			item.save()
			# se traen todas las medallas asignadas
			awards = Award.objects.filter(badge=badge)
			# se eliminan las tuplas de medallas asignadas ya que hay mas material
			awards.delete()


# cada vez que se cree o elimine una evaluacion o actividad aumenta o disminuye los puntos para ganarse la medalla 
@receiver(calculate_points_end_badge)
def points_end_badge(sender, badge, points, action, element, instance_element, **kwargs):
	print 'points_end_badge'
	b = get_badge(badge)
	if action == 'add':
		b.points_end += points
		b.save()
		verify_remove_for_award(b)
	elif action == 'remove':
		b.points_end -= points
		b.save()
		verify_users_for_award(b, element, instance_element)


#-------------------------------------------
# funcion para asignar los puntos
def set_points(progress, points, badge, user):
	
	# si es menor que 100 aumenta los puntos 
	# si es mayor recalcula el progreso del usuario al crearse nuevo material
	
	if progress.percent < 100.0:
		progress.increment_by(points)
		progress.update_percent2()
		progress.save()

# de aqui para abajo acomodar notificaciones 
		if progress.percent >= 100:
			print 'me gane la medalla'
			gamification_badge_award.send(sender=set_points, badge=badge, user= user)
			#action.send(user, verb='badge', action_object=badge, target=badge)

			#---------------------------------------------------------------
			#lista todas las medallas 
			#badges = list(Badge.objects.order_by('prerequisites').all())
			#medalla del usuario recien asignada
			#badge_user =  progress.badge 
			# indice de la medalla en la lista 
			#i = badges.index(badge_user)
			# se pasa a la siguiente medalla si existe 
			#if i <= len(badges)-1:
				#progress.percent = 0
				#progress.counter = 0
				#progress.badge = badges[i+1]
				#progress.save()
		

	else:
		progress.update_percent2()
		progress.save()
		# envio notificacion de que hay nuevo material y se ha quitado la medalla 
		
		#lista todas las medallas 
		#badges = list(Badge.objects.order_by('prerequisites').all())
		#medalla del usuario recien asignada
		#badge_user =  progress.badge 
		# indice de la medalla en la lista 
		#i = badges.index(badge_user)
		# se pasa a la siguiente medalla si existe 
		#if i <= len(badges)-1:
		#	progress.percent = 0
		#	progress.counter = 0
		#	progress.badge = badges[i+1]
		#	progress.save()


# puntos del quiz 
@receiver(post_points_quiz, sender=Sitting_Serializer)
def set_points_quiz(sender, sitting, badge, **kwargs):
	
	# si aprobo el quiz 
	if sitting.check_if_passed == True:
		print 'puntos quices'
		
		# se trae la medalla y el progreso del usario en esa medalla
		b = get_badge(badge)
		p = b.progress_for(sitting.user)

		# se consulta cuantos puntos tiene ese quiz 
		points = Scores.objects.get(id_event=sitting.quiz.id)

		# se llama a la funcion para asigna los puntos en el progreso 
		set_points(p, points.score, b, sitting.user)
			

from wiki.views import RequestApproveView

# puntos de la wiki  
@receiver(post_points_wiki, sender=RequestApproveView)
def set_points_wiki(sender, user, badge, **kwargs):
	print 'hola puntos de la wiki'
	print user
	#b = get_badge(badge)
	#p = b.progress_for(user)
	#p = Progress.objects.get( user = user)
	#set_points(p)
	

from activitie.views import ActivitieChildCheckView

# puntos de las actvidades  
@receiver(post_points_activity, sender = ActivitieChildCheckView)
def set_points_activitie(sender, user, badge, activitie, **kwargs):
	print 'set_points_activitie'
	# se trae la medalla y el progreso del usario en esa medalla
	b = get_badge(badge)
	p = b.progress_for(user)
	# se consulta cuantos puntos tiene ese quiz 
	points = Scores.objects.get(id_event=activitie)

	# se llama a la funcion para asigna los puntos en el progreso 
	set_points(p, points.score, b, user)
