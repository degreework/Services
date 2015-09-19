from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType

from notifications import notify

from post_framework.models import Thread
from forum.serializers import AnswerCreateSerializer, UpdateAskSelializer
from comment.serializers import CreateCommentSerializer
from wiki.views import RequestApproveView
from wiki.receivers import generate_request

from forum.models import Answer
from users.models import User

from .signals import forum_answered, forum_ask_updated, post_comment, wiki_request_checked, wiki_request_created


"""FORUM"""
@receiver(forum_answered, sender=AnswerCreateSerializer)
def forum_generate_answer(sender, ask, answer, author, **kwargs):

	if ask.author != author:
		notify.send(
			author,
			recipient=ask.author,
			verb=u'has been answered',
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
			verb=u'has been updated',
	        action_object=ask,
	        #description=u'Description',
	        target=ask)

"""COMENT"""
@receiver(post_comment, sender=CreateCommentSerializer)
def post_generate_comment(sender, post, comment, author, **kwargs):
	post = Thread.objects.get_subclass(id=post.id)

	if post.author != author:
		notify.send(
			author,
			recipient=post.author,
			verb=u'has been commented',
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
			verb=u'has been checked',
	        action_object=request,
	        #description=u'Description',
	        target=request)


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
			verb=u'has edited a wiki page',
	        action_object=request,
	        description=request.message,
	        target=request)