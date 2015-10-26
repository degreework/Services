from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from notifications.models import Notification

from comment.models import Comment
from forum.models import Answer, Ask
from wiki.models import Request
from badger.models import Badge


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

		return target
	
	class Meta():
	        model = Notification
	        fields = ('id', 'level', 'actor', 'target', 'unread', 'verb', 'timestamp', 'description')
	        read_only_fields = fields