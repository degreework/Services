# -*- encoding: utf-8 -*-

from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType

from notifications import notify
from notifications.models import Notification

from post_framework.models import Thread
from forum.serializers import AnswerCreateSerializer, UpdateAskSelializer
from comment.serializers import CreateCommentSerializer
from wiki.views import RequestApproveView
from wiki.receivers import generate_request

#----------------------------------------------
from gamification.receivers import set_points
#----------------------------------------------

from forum.models import Answer
from users.models import User
from quiz.models import Quiz
from activitie.models import ActivitieParent

from .signals import forum_answered, forum_ask_updated, post_comment, wiki_request_checked, wiki_request_created, gamification_badge_award, create_remove_action, activitie_checked


"""FORUM"""
@receiver(forum_answered, sender=AnswerCreateSerializer)
def forum_generate_answer(sender, ask, answer, author, **kwargs):

	if ask.author != author:
		notify.send(
			author,
			recipient=ask.author,
			verb=u'se ha dado respuesta',
	        action_object=answer,
	        #description=u'Description',
	        target=ask)

@receiver(forum_ask_updated, sender=UpdateAskSelializer)
def forum_updated(sender, ask, **kwargs):
	authors = []

	for answer in Answer.objects.filter(ask=ask):
		if not answer.author in authors:
			if answer.author != ask.author:
				authors.append(answer.author)

	for author in authors:
		notify.send(
			ask.author,
			recipient=author,
			verb=u'ha sido actualizado',
	        action_object=ask,
	        #description=u'Description',
	        target=ask)

"""COMENT"""
from wiki.models import pageComments
@receiver(post_comment, sender=CreateCommentSerializer)
def post_generate_comment(sender, post, comment, author, **kwargs):
	post = Thread.objects.get_subclass(id=post.id)
	
	if ContentType.objects.get_for_model(post) is ContentType.objects.get_for_model(pageComments):
		return None
	else:
		if post.author != author:
			notify.send(
				author,
				recipient=post.author,
				verb=u'ha sido comentado',
		        action_object=comment,
		        #description=u'Description',
		        target=post)


"""WIKI"""
@receiver(wiki_request_checked, sender=RequestApproveView)
def wiki_request_checked(sender, request, **kwargs):
	
	if request.checked_by != request.created_by:
		
		notify.send(
			request.checked_by,
			recipient=request.created_by,
			verb=u'ha sido aprobado',
	        action_object=request,
	        #description=u'Description',
	        target=request)
		
	#elimina la notificacion (wiki_request_created) del created request
	"""
		#user who to perform action
		for noti in Notification.objects.filter(
			actor_object_id=request.created_by,
			target_object_id=request.id,
			recipient=request.checked_by):
			print noti
			noti.mark_as_read()

		#all teachers who received request notification
		#for now is to superusers but must be to teachers
		for user in User.objects.filter(is_superuser=True):
			for noti in Notification.objects.filter(
				actor_object_id=request.created_by,
				target_object_id=request.id,
				recipient=user):
				print noti
				noti.mark_as_read()
	"""


#from waliki.git.views import version as git_version
@receiver(wiki_request_created, sender=generate_request)
def wiki_request_created(sender, request, **kwargs):
	#version = git_version(request._request, slug=request.page.slug, version=request.commit, raw=True)
	users = []

	#for now is to superusers but must be to teachers
	for user in User.objects.filter(is_superuser=True):
		if user != request.created_by:
			users.append(user)
	
	for user in users:
		notify.send(
			request.created_by,
			recipient=user,
			verb=u'una pagina de la wiki ha sido editada',
	        action_object=request,
	        description=request.message,
	        target=request)


"""GAMIFICATION"""
@receiver(gamification_badge_award, sender=set_points)
def gamification_badge_award(sender, badge, user, **kwargs):
	#print 'gamification_badge_award'
	notify.send(
			user,
			recipient=user,
			verb=u' Felicitaciones ganaste la medalla',
	        action_object=badge,
	        #description=request.message,
	        target=badge)

@receiver(create_remove_action)
def create_remove_action(sender, author, action, instance, **kwargs):

	
	for user in User.objects.all():
		if action == 'add':
			
			notify.send(
				author,
				recipient=user,
				verb=u' se ha creado',
		        action_object=instance,
		        #description=request.message,
		        target=instance)

		elif action == 'remove':
			
			notify.send(
					author,
					recipient=user,
					verb=u' se ha eliminado',
			        action_object=instance,
			        #description=request.message,
			        target= instance)

from .signals import create_module
from module.serializers import ModuleSerializer

@receiver(create_module, sender=ModuleSerializer)
def created_module(sender, author, module, **kwargs):
	users = User.objects.all()
	for user in users:
		notify.send(
			author,
			recipient=user,
			verb=u'ha creado un módulo',
	        action_object=module,
	        #description=request.message,
	        target=module)

from activitie.views import ActivitieChildCheckView
@receiver(activitie_checked, sender=ActivitieChildCheckView)
def activitie_checked(sender, checker, activitie, **kwargs):
	print "notificacion activitie checked"
	print activitie
	notify.send(
		checker,
		recipient=activitie.author,
		verb=u'ha revisado',
        action_object=activitie,
        #description=request.message,
        target=activitie)
	

from django.db.models.signals import pre_delete
from waliki.models import Page
from notifications.models import Notification

@receiver(pre_delete, sender=Page)
def log_deleted_page(sender, instance, using, **kwargs):
	"""
	if a Page is deleted, Notification must be deleted too
	"""
	page_type = ContentType.objects.get(model="request")
	Notification.objects.filter(target_content_type=page_type).delete()