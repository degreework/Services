from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from notifications.models import Notification

from comment.models import Comment
from forum.models import Answer, Ask
from wiki.models import Request
from badger.models import Badge
from quiz.models import Quiz
from activitie.models import ActivitieParent, ActivitieChild
from module.models import Module, Activitie_wrap
from django.shortcuts import get_list_or_404


class NotificationSerializer(serializers.ModelSerializer):
	"""docstring for ClassName"""

	actor = serializers.SerializerMethodField()
	target = serializers.SerializerMethodField()

	def get_actor(self, obj):
		return {'id': obj.actor_object_id, 'name': obj.actor.get_full_name()}

	def get_target(self, obj):
		content_type = obj.target_content_type
		target = {}

		if content_type == ContentType.objects.get_for_model(Ask):
			ask = Ask.objects.get(id=obj.target.id)
			target = {
			'id': ask.id,
			'type': u'Ask',
			'detail': ask.title
			}
		
		elif content_type == ContentType.objects.get_for_model(Answer):
			answer = Answer.objects.get(id=obj.target.id)
			target = {
			'id': answer.id,
			'type': u'Answer',
			'detail': answer.text[:8]
			}

		elif content_type == ContentType.objects.get_for_model(Request):
			request = Request.objects.get(id=obj.target.id)
			target = {
			'id': request.id,
			'type': u'Request',
			'detail': { 
				'approved':request.approved,
				'page': {
					#'id': request.page.id,
					'slug': request.page.slug,
					'title': request.page.title,
					'commit': request.commit
					}
				}
			}

		elif content_type == ContentType.objects.get_for_model(Badge):
			print 'entro en el badge'
			badge = Badge.objects.get(id = obj.target.id)
			target = {
			'id': badge.id,
			'type': u'Badge',
			'detail': badge.title
			}

		elif content_type ==ContentType.objects.get_for_model(Quiz):
			print 'entro en el quiz'
			if obj.target != None:	
				quiz = Quiz.objects.get(id = obj.target.id)
				target = {
				'id': quiz.id,
				'type': u'Quiz',
				'detail': quiz.title
				}
			else:
				target = {
				'id': '',
				'type': u'Activitie',
				'detail': ''
				}

		elif content_type ==ContentType.objects.get_for_model(ActivitieParent):
			print 'entro en el activitie'
					
			if obj.target != None:	
				activitie = ActivitieParent.objects.get(id = obj.target.id)
				print activitie
				target = {
				'id': activitie.id,
				'type': u'Activitie',
				'detail': activitie.name
				}	
			else:
				target = {
				'id': '',
				'type': u'Activitie',
				'detail': ''
				}

		elif content_type == ContentType.objects.get_for_model(ActivitieChild):
			module = Activitie_wrap.objects.filter(activitie=obj.target.parent)[0].module
			target = {
				'id': obj.target.parent.id,
				'type': u'Activitie',
				'detail': obj.target.parent.name,
				'module':{
					'id': module.id,
					'name': module.name,
					'slug': module.slug
				}
			}

		elif content_type == ContentType.objects.get_for_model(Module):
			target = {
			'id': obj.target.id,
			'type': u'Module',
			'detail': obj.target.name,
			'slug': obj.target.slug
			}
			
			
			

		return target
	
	class Meta():
	        model = Notification
	        fields = ('id', 'level', 'actor', 'target', 'unread', 'verb', 'timestamp', 'description')
	        read_only_fields = fields