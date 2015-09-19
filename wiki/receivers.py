from django.dispatch import receiver
from .models import Request

from .signals import page_request

from django.conf import settings
from reminder.signals import wiki_request_created

@receiver(page_request, sender=Request)
def generate_request(sender, page, commit, author, message, **kwargs):
    request = Request(page=page, commit=commit, checked_by=None, created_by=author, message=message)
    request.save()
    if getattr(settings, 'NOTIFICATIONS', False):
    	wiki_request_created.send(sender=generate_request, request=request)
