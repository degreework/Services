from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from notifications.models import Notification

from comment.models import Comment
from forum.models import Answer, Ask
from wiki.models import Request
from badger.models import Badge
from quiz.models import Quiz
from activitie.models import ActivitieParent, ActivitieChild
from module.models import Module, Activitie_wrap, Wiki_wrap, Quiz_wrap, Forum_wrap
from django.shortcuts import get_list_or_404


class NotificationSerializer(serializers.ModelSerializer):
	"""docstring for ClassName"""

	actor = serializers.SerializerMethodField()
	target = serializers.SerializerMethodField()

	def get_actor(self, obj):
		return {'id': obj.actor_object_id, 'name': obj.actor.get_full_name()}

	def get_target(self, obj):
		#print "get target"
		#print obj.action
		#print obj.target_content_type
		content_type = obj.target_content_type
		target = {}

		if content_type == ContentType.objects.get_for_model(Ask):
			ask = obj.target

			wrap = Forum_wrap.objects.filter(ask=obj.target)[0]
			target = {
			'id': ask.id,
			'type': u'Ask',
			'detail': ask.title,
			'module':{
						'id': wrap.module.id,
						'name': wrap.module.name,
						'slug': wrap.module.slug	
					}
			}
		
		elif content_type == ContentType.objects.get_for_model(Answer):
			answer = Answer.objects.get(id=obj.target.id)
			target = {
			'id': answer.id,
			'type': u'Answer',
			'detail': answer.text[:8]
			}

		elif content_type == ContentType.objects.get_for_model(Request):
				wrap = Wiki_wrap.objects.filter(page=obj.target.page)[0]
				target = {
				'id': obj.target.id,
				'type': u'Request',
				'detail': { 
					'approved': obj.target.approved,
					'page': {
						#'id': request.page.id,
						'slug': obj.target.page.slug,
						'title': obj.target.page.title,
						'commit': obj.target.commit
						}
					},
				'module':{
						'id': wrap.module.id,
						'name': wrap.module.name,
						'slug': wrap.module.slug
						
					}
				}

		elif content_type == ContentType.objects.get_for_model(Badge):
			#print 'entro en el badge'
			badge = Badge.objects.get(id = obj.target.id)
			target = {
			'id': badge.id,
			'type': u'Badge',
			'detail': badge.title
			}

		elif content_type ==ContentType.objects.get_for_model(Quiz):
			
			if obj.target != None:	
				wrap = Quiz_wrap.objects.filter(quiz=obj.target)[0]
				
				target = {
					'id': obj.target.id,
					'type': u'Quiz',
					'detail': obj.target.title,
					'module':{
						'id': wrap.module.id,
						'name': wrap.module.name,
						'slug': wrap.module.slug
					}
				}
			else:
				target = {
				'id': '',
				'type': u'Activitie',
				'detail': ''
				}

		elif content_type ==ContentType.objects.get_for_model(ActivitieParent):
			
			if obj.target != None:	
				wrap = Activitie_wrap.objects.filter(activitie=obj.target)[0]
				target = {
				'id': wrap.activitie.id,
				'type': u'Activitie',
				'detail': wrap.activitie.name,
				'module':{
					'id': wrap.module.id,
					'name': wrap.module.name,
					'slug': wrap.module.slug
					}
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